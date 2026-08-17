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

        # Servir archivos estáticos del frontend
        dir_web = obtener_ruta_assets_web()
        if path == "/" or path == "":
            ruta_target = dir_web / "index.html"
        else:
            rel_path = path.lstrip("/")
            ruta_target = dir_web / rel_path

        if ruta_target.exists() and ruta_target.is_file():
            self._responder_archivo(ruta_target)
        else:
            self.send_error(404, "Página no encontrada")

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

            elif path == "/api/revisor/verificar":
                from src.services.revisor_service import RevisorService
                resultado = RevisorService.verificar_equipo(body)
                self._responder_json({
                    "status": "ok",
                    "resultado": resultado
                })

            elif path == "/api/revisor/generar_plantilla":
                from src.services.revisor_service import RevisorService
                plantilla = RevisorService.generar_plantilla_texto(body)
                self._responder_json({
                    "status": "ok",
                    "plantilla_texto": plantilla
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
