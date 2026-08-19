from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import mimetypes
from pathlib import Path
import urllib.parse
from datetime import datetime
import traceback
import sys
import socket

from src.services.certificado_service import CertificadoService
from src.services.portal_service import PortalService
from src.utils.autofill import procesar_autofill
from src.pdf.generador_pdf import GeneradorPDF


def obtener_ruta_assets_web() -> Path:
    """Retorna la ruta absoluta al directorio de assets web (compatible con PyInstaller)."""
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent.parent.parent
    return base / "assets" / "web"


class CertificadoHTTPHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """Silenciar logs HTTP excesivos en consola para mantenerla limpia."""
        pass

    def _responder_json(self, datos: dict, codigo: int = 200):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def _responder_archivo(self, ruta: Path, content_type: str | None = None, filename: str | None = None):
        if not ruta.exists() or not ruta.is_file():
            self.send_error(404, "Archivo no encontrado")
            return

        if not content_type:
            guessed_type, _ = mimetypes.guess_type(str(ruta))
            content_type = guessed_type or "application/octet-stream"

        contenido = ruta.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8" if any(t in content_type for t in ["text", "javascript", "json", "css"]) else content_type)
        if content_type == "application/pdf":
            fname = filename or ruta.name
            self.send_header("Content-Disposition", f'inline; filename="{fname}"')
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/list":
            query = urllib.parse.parse_qs(parsed.query)
            año = int(query.get("año", [datetime.now().year])[0])
            certificados = CertificadoService.listar_certificados(año)
            self._responder_json({"status": "ok", "año": año, "certificados": certificados})
            return

        if path == "/api/bitacora":
            bitacora = PortalService.obtener_bitacora()
            self._responder_json({"status": "ok", **bitacora})
            return

        if path == "/api/asistentes":
            asistentes = PortalService.obtener_asistentes()
            self._responder_json({"status": "ok", "asistentes": asistentes})
            return

        if path == "/api/destinatarios":
            destinatarios = PortalService.obtener_destinatarios()
            self._responder_json({"status": "ok", "destinatarios": destinatarios})
            return

        if path == "/api/fechas_fin_semana":
            sab, dom, sem = PortalService.calcular_fechas_fin_semana_actual()
            self._responder_json({"status": "ok", "fecha_sabado": sab, "fecha_domingo": dom, "semana": sem})
            return

        if path == "/api/wiki/buscar":
            query = urllib.parse.parse_qs(parsed.query)
            q = query.get("q", [""])[0]
            res = PortalService.buscar_trac_wiki(q)
            self._responder_json({"status": "ok", **res})
            return

        if path == "/api/wiki/indice":
            res = PortalService.obtener_indice_trac_wiki()
            self._responder_json({"status": "ok", **res})
            return

        if path == "/api/music/status":
            # Estado del reproductor
            status_data = {"status": "stopped", "title": "Portal de Soporte Innovex", "artist": "Música Host"}
            try:
                res_st = subprocess.run(["playerctl", "status"], capture_output=True, text=True, timeout=2)
                if res_st.returncode == 0:
                    status_data["status"] = res_st.stdout.strip().lower()
                    t_st = subprocess.run(["playerctl", "metadata", "title"], capture_output=True, text=True, timeout=2)
                    if t_st.returncode == 0 and t_st.stdout.strip():
                        status_data["title"] = t_st.stdout.strip()
                    a_st = subprocess.run(["playerctl", "metadata", "artist"], capture_output=True, text=True, timeout=2)
                    if a_st.returncode == 0 and a_st.stdout.strip():
                        status_data["artist"] = a_st.stdout.strip()
            except Exception:
                pass
            self._responder_json(status_data)
            return

        if path == "/api/music/control":
            query = urllib.parse.parse_qs(parsed.query)
            action = query.get("action", [""])[0]
            q_search = query.get("query", [""])[0]
            commands = {
                "volup": ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"],
                "voldn": ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"],
                "mute": ["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"],
                "play": ["playerctl", "play-pause"],
                "next": ["playerctl", "next"],
                "prev": ["playerctl", "previous"]
            }
            if action in commands:
                try:
                    subprocess.run(commands[action], timeout=3)
                    self._responder_json({"status": "ok"})
                except Exception as exc:
                    self._responder_json({"status": "error", "message": str(exc)})
                return
            self._responder_json({"status": "ok"})
            return

        if path.startswith("/api/pdf_preview/"):
            # Servir PDF generado para previsualización directa en la web
            partes = path.replace("/api/pdf_preview/", "").split("/")
            if len(partes) >= 2:
                año = partes[0]
                location = partes[1]
                nombre_pdf = f"certificado_inst_{location}.pdf"
                dir_location = Path("storage/certificados") / año / location

                posibles = [
                    dir_location / nombre_pdf,
                    dir_location / "certificado.pdf"
                ]
                for p in posibles:
                    if p.exists() and p.is_file():
                        self._responder_archivo(p, "application/pdf", filename=nombre_pdf)
                        return
            self.send_error(404, "PDF no encontrado")
            return

        # Servir archivos estáticos del frontend y assets corporativos
        dir_web = obtener_ruta_assets_web()
        dir_assets = dir_web.parent
        if path == "/" or path == "":
            ruta_target = dir_web / "index.html"
        elif path.startswith("/assets/"):
            rel_asset = path[len("/assets/"):]
            ruta_target = dir_assets / rel_asset
        else:
            rel_path = path.lstrip("/")
            ruta_target = dir_web / rel_path
            if not (ruta_target.exists() and ruta_target.is_file()):
                posible_asset = dir_assets / rel_path
                if posible_asset.exists() and posible_asset.is_file():
                    ruta_target = posible_asset

        if ruta_target.exists() and ruta_target.is_file():
            self._responder_archivo(ruta_target)
        else:
            self.send_error(404, f"Archivo no encontrado: {path}")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length)
            
            body = {}
            if raw_body and ("json" in self.headers.get("Content-Type", "").lower() or path.startswith("/api/")):
                try:
                    body = json.loads(raw_body.decode("utf-8"))
                except Exception:
                    body = {}

            if path == "/api/autofill":
                texto = body.get("texto", "")
                certificado_actual = body.get("certificado", {})
                resultado = procesar_autofill(certificado_actual, texto)
                self._responder_json({"status": "ok", "certificado": certificado_actual, "resumen": resultado.get("resumen", [])})

            elif path == "/api/save":
                certificado = body.get("certificado", {})
                datos_gen = certificado.get("datos_generales", {})
                location = datos_gen.get("location") or "sin_location"
                año = datetime.now().year
                
                ruta_json = CertificadoService.guardar_certificado(certificado, location, año)
                # Copiar evidencias si existen en ~/evidencias_instalacion
                CertificadoService.copiar_evidencias_a_certificado(location, año)
                
                self._responder_json({
                    "status": "ok",
                    "mensaje": "Certificado guardado correctamente",
                    "ruta": str(ruta_json),
                    "location": location,
                    "año": año
                })

            elif path == "/api/generate_pdf":
                certificado = body.get("certificado", {})
                datos_gen = certificado.get("datos_generales", {})
                location = datos_gen.get("location") or "sin_location"
                año = datetime.now().year

                dir_cert = Path("storage/certificados") / str(año) / location
                dir_cert.mkdir(parents=True, exist_ok=True)
                
                ruta_json = CertificadoService.guardar_certificado(certificado, location, año)
                CertificadoService.copiar_evidencias_a_certificado(location, año)

                nombre_pdf = f"certificado_inst_{location}.pdf"
                ruta_pdf = dir_cert / nombre_pdf
                dir_evidencias = dir_cert / "evidencias"

                GeneradorPDF().generar(
                    certificado,
                    str(ruta_pdf),
                    carpeta_evidencias=dir_evidencias if dir_evidencias.exists() else None
                )

                pdf_preview_url = f"/api/pdf_preview/{año}/{location}/{nombre_pdf}"
                
                self._responder_json({
                    "status": "ok",
                    "mensaje": "PDF generado con éxito",
                    "ruta_pdf": str(ruta_pdf),
                    "pdf_preview_url": pdf_preview_url
                })

            elif path == "/api/load":
                location = body.get("location")
                año = int(body.get("año", datetime.now().year))
                if not location:
                    self._responder_json({"status": "error", "mensaje": "Location es requerido"}, 400)
                    return

                try:
                    cert_data = CertificadoService.cargar_certificado(location, año)
                    self._responder_json({"status": "ok", "certificado": cert_data})
                except FileNotFoundError:
                    self._responder_json({"status": "error", "mensaje": f"No se encontró certificado para {location}"}, 404)

            elif path == "/api/delete":
                location = body.get("location") or body.get("datos_generales", {}).get("location")
                año = int(body.get("año", datetime.now().year))
                if not location:
                    self._responder_json({"status": "error", "mensaje": "Location es requerido"}, 400)
                    return

                exito = CertificadoService.eliminar_certificado(location, año)
                if exito:
                    self._responder_json({
                        "status": "ok",
                        "mensaje": f"Certificado de {location} eliminado correctamente",
                        "location": location
                    })
                else:
                    self._responder_json({"status": "error", "mensaje": f"No se encontró el certificado de {location}"}, 404)

            elif path == "/api/upload_evidencia":
                nombre = body.get("nombre", "foto.jpg")
                base64_data = body.get("base64", "")
                location = body.get("location", "sin_location")
                
                if "," in base64_data:
                    base64_data = base64_data.split(",", 1)[1]
                    
                import base64
                file_bytes = base64.b64decode(base64_data)
                
                dir_ev = Path("storage/certificados/2026") / location / "evidencias"
                dir_ev.mkdir(parents=True, exist_ok=True)
                
                dest_file = dir_ev / nombre
                dest_file.write_bytes(file_bytes)
                
                self._responder_json({
                    "status": "ok",
                    "mensaje": "Evidencia subida correctamente",
                    "ruta": str(dest_file),
                    "nombre": nombre
                })

            elif path == "/api/upload_alarmas":
                nombre = body.get("nombre", "alarmas.xlsx")
                base64_data = body.get("base64", "")
                location = body.get("location", "sin_location")
                
                if "," in base64_data:
                    base64_data = base64_data.split(",", 1)[1]
                    
                import base64
                from src.utils.excel_parser import parsear_alarmas_excel
                
                file_bytes = base64.b64decode(base64_data)
                dir_ev = Path("storage/certificados/2026") / location / "evidencias"
                dir_ev.mkdir(parents=True, exist_ok=True)
                
                dest_file = dir_ev / nombre
                dest_file.write_bytes(file_bytes)
                
                alarmas = parsear_alarmas_excel(dest_file)
                self._responder_json({
                    "status": "ok",
                    "mensaje": "Planilla de alarmas procesada",
                    "alarmas": alarmas
                })

            elif path == "/api/parse_alarmas_texto":
                texto = body.get("texto", "")
                from src.utils.excel_parser import parsear_alarmas_texto
                alarmas = parsear_alarmas_texto(texto)
                self._responder_json({
                    "status": "ok",
                    "mensaje": f"{len(alarmas)} alarmas procesadas",
                    "alarmas": alarmas
                })

            elif path == "/api/ssh_autofill":
                from src.services.revisor_service import RevisorService
                from src.constants.empresas import parse_location_info
                try:
                    salida_ssh = RevisorService.ejecutar_ssh_autofill(body)
                    certificado = body.get("certificado", {})
                    host = body.get("host", "").strip()
                    clave = body.get("clave", "").strip()
                    
                    if body.get("limpiar_previos", False):
                        certificado["motes"] = []
                        certificado["ubicaciones"] = []
                        certificado["equipos_repuesto"] = []
                        certificado["configuracion_alarmas"] = []

                    if host:
                        emp, nom_c = parse_location_info(host)
                        if "datos_generales" not in certificado:
                            certificado["datos_generales"] = {}
                        loc_clean = host.split(".")[0].strip().lower()
                        certificado["datos_generales"]["location"] = loc_clean
                        if nom_c:
                            certificado["datos_generales"]["nombre_centro"] = nom_c
                        if emp:
                            certificado["datos_generales"]["empresa"] = emp
                        if "infraestructura" not in certificado:
                            certificado["infraestructura"] = {}
                        certificado["infraestructura"]["pc_id"] = host
                        if clave:
                            certificado["infraestructura"]["pc_password"] = clave

                    resumen_dict = procesar_autofill(certificado, salida_ssh)

                    # Asegurar coherencia de location y nombre_centro post autofill
                    if host:
                        emp, nom_c = parse_location_info(host)
                        loc_clean = host.split(".")[0].strip().lower()
                        if not certificado.get("datos_generales"):
                            certificado["datos_generales"] = {}
                        certificado["datos_generales"]["location"] = loc_clean
                        if nom_c and (not certificado["datos_generales"].get("nombre_centro") or certificado["datos_generales"].get("nombre_centro") == loc_clean.upper()):
                            certificado["datos_generales"]["nombre_centro"] = nom_c
                        if emp and not certificado["datos_generales"].get("empresa"):
                            certificado["datos_generales"]["empresa"] = emp

                    self._responder_json({
                        "status": "ok",
                        "certificado": certificado,
                        "resumen": resumen_dict.get("resumen", []),
                        "exito": resumen_dict.get("exito", False)
                    })
                except Exception as exc:
                    self._responder_json({
                        "status": "error",
                        "mensaje": str(exc)
                    })

            elif path == "/api/revisor/verificar":
                from src.services.revisor_service import RevisorService
                resultado = RevisorService.verificar_equipo(body)
                if resultado.get("error") and not resultado.get("log_cacheton_raw") and not resultado.get("status_raw") and not resultado.get("motes_raw") and not resultado.get("motes_texto_raw"):
                    self._responder_json({
                        "status": "error",
                        "mensaje": f"Error de conexión: {resultado.get('error')}",
                        "resultado": resultado
                    })
                else:
                    self._responder_json({
                        "status": "ok",
                        "resultado": resultado
                    })

            elif path == "/api/revisor/generar_plantilla":
                from src.services.revisor_service import RevisorService
                plantilla = RevisorService.generar_plantilla_texto(body)
                html_doc = RevisorService.generar_documento_live_html(body)
                self._responder_json({
                    "status": "ok",
                    "plantilla_texto": plantilla,
                    "documento_live_html": html_doc
                })

            elif path == "/api/revisor/ingreso_tecnico":
                from src.services.revisor_service import RevisorService
                resultado = RevisorService.consultar_ingreso_tecnico_remoto(body)
                self._responder_json({
                    "status": "ok",
                    "resultado": resultado
                })

            elif path == "/api/revisor/generar_plantilla_ingreso":
                from src.services.revisor_service import RevisorService
                plantilla = RevisorService.generar_plantilla_ingreso_tecnico(body)
                html_doc = RevisorService.generar_documento_ingreso_tecnico_html(body)
                self._responder_json({
                    "status": "ok",
                    "plantilla_texto": plantilla,
                    "documento_live_html": html_doc
                })

            elif path == "/api/bitacora":
                texto = body.get("texto", "")
                res = PortalService.actualizar_bitacora(texto)
                self._responder_json(res)

            elif path == "/api/destinatarios":
                action = body.get("action", "")
                if action == "toggle_destinatario":
                    dest_id = int(body.get("id", 0))
                    activo = bool(body.get("activo", True))
                    res = PortalService.toggle_destinatario(dest_id, activo)
                    self._responder_json(res)
                elif action == "create":
                    empresa = body.get("empresa", "")
                    correo = body.get("correo", "")
                    res = PortalService.crear_destinatario(empresa, correo)
                    self._responder_json(res)
                elif action == "delete_destinatario":
                    dest_id = int(body.get("id", 0))
                    res = PortalService.eliminar_destinatario(dest_id)
                    self._responder_json(res)
                else:
                    self._responder_json({"status": "error", "mensaje": "Acción desconocida"}, 400)

            elif path == "/api/enviar_correos_masivos":
                personal_id = body.get("personal_id")
                fecha_sabado = body.get("fecha_sabado") or ""
                fecha_domingo = body.get("fecha_domingo") or ""
                correo_prueba = body.get("correo_prueba", "").strip()

                asistentes = PortalService.obtener_asistentes()
                personal = next((p for p in asistentes if str(p.get("id")) == str(personal_id)), None)
                if not personal and asistentes:
                    personal = asistentes[0]
                elif not personal:
                    personal = {"nombre": "Asistente de Soporte", "cargo": "ASISTENTE DE SOPORTE", "telefono": "+56 9 8419 4843", "correo": "soporte@innovex.cl"}

                html_content = PortalService.generar_html_correo_fin_semana(personal, fecha_sabado, fecha_domingo)
                destinatarios = PortalService.obtener_destinatarios()
                activos = [d for d in destinatarios if d.get("activo")]

                self._responder_json({
                    "status": "ok",
                    "mensaje": f"Correo generado exitosamente para {len(activos)} destinatarios activos." if not correo_prueba else f"Modo prueba: correo generado para {correo_prueba}.",
                    "html_correo": html_content,
                    "destinatarios_count": len(activos),
                    "personal": personal,
                    "modo_prueba": bool(correo_prueba)
                })

            else:
                self._responder_json({"status": "error", "mensaje": "Endpoint no encontrado"}, 404)

        except Exception as e:
            traceback.print_exc()
            self._responder_json({"status": "error", "mensaje": str(e)}, 500)


def obtener_ips_locales() -> list[str]:
    """Retorna las direcciones IP v4 locales de las interfaces de red activas."""
    ips = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_principal = s.getsockname()[0]
        s.close()
        if ip_principal and not ip_principal.startswith("127."):
            ips.append(ip_principal)
    except Exception:
        pass

    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith("127.") and ip not in ips:
                ips.append(ip)
    except Exception:
        pass

    return ips


def iniciar_servidor_http(host: str = "0.0.0.0", puerto: int = 8888):
    """Inicia el servidor HTTP en el host y puerto especificados."""
    puerto_actual = puerto
    while puerto_actual < puerto + 20:
        try:
            server = HTTPServer((host, puerto_actual), CertificadoHTTPHandler)
            ips = obtener_ips_locales()
            print(f"🚀 Servidor Live activo en el puerto {puerto_actual}:")
            print(f"   • Local (este equipo):  http://localhost:{puerto_actual}/")
            if host in ("0.0.0.0", ""):
                if ips:
                    for ip in ips:
                        print(f"   • Red Local (colegas):  http://{ip}:{puerto_actual}/")
                else:
                    print(f"   • Red Local (colegas):  http://<IP-de-tu-equipo>:{puerto_actual}/")
            else:
                print(f"   • Host específico:      http://{host}:{puerto_actual}/")
            return server, puerto_actual
        except OSError:
            puerto_actual += 1
    
    raise RuntimeError("No se pudo encontrar un puerto libre entre 8888 y 8908.")
