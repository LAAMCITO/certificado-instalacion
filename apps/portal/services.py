"""
Service centralizado para el Portal de Soporte Innovex (Django ORM + SQLite).
"""

import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Asistente, Destinatario, Bitacora, EncargadoArea, ZonaGeografica, Tecnico


# Asistentes de soporte por defecto basados en la dotación de Innovex
ASISTENTES_DEFAULT = [
    {"nombre": "Felipe Godoy", "cargo": "ASISTENTE DE SOPORTE", "telefono": "+56 9 4457 4128", "correo": "felipe.godoy@innovex.cl", "orden": 1},
    {"nombre": "Hector Portillo", "cargo": "ASISTENTE DE SOPORTE", "telefono": "+56 9 8419 4843", "correo": "hector.portillo@innovex.cl", "orden": 2},
    {"nombre": "Ivan Soto", "cargo": "ASISTENTE DE SOPORTE", "telefono": "+56 9 3198 5778", "correo": "ivan.soto@innovex.cl", "orden": 3},
    {"nombre": "Edwin Gonzalez", "cargo": "ASISTENTE DE SOPORTE", "telefono": "+56 9 4259 7333", "correo": "edwin.gonzalez@innovex.cl", "orden": 4},
    {"nombre": "Leonardo Araneda", "cargo": "ASISTENTE DE SOPORTE", "telefono": "+56 9 8419 4913", "correo": "leonardo.araneda@innovex.cl", "orden": 5},
    {"nombre": "Gabriel Moya", "cargo": "ASISTENTE DE SOPORTE", "telefono": "+56 9 5698 9299", "correo": "gabriel.moya@innovex.cl", "orden": 6},
    {"nombre": "Leonidas Yungue", "cargo": "ASISTENTE DE SOPORTE", "telefono": "+56 9 6236 5854", "correo": "leonidas.yungue@innovex.cl", "orden": 7},
]

# Destinatarios y empresas acuícolas iniciales
DESTINATARIOS_DEFAULT = [
    {"empresa": "CERMAQ", "correo": "soporte.cermaq@innovex.cl", "activo": True},
    {"empresa": "CERMAQ", "correo": "operaciones.cermaq@cermaq.com", "activo": True},
    {"empresa": "AQUACHILE", "correo": "soporte.aquachile@innovex.cl", "activo": True},
    {"empresa": "AQUACHILE", "correo": "monitoreo.centros@aquachile.com", "activo": True},
    {"empresa": "BLUMAR", "correo": "soporte.blumar@innovex.cl", "activo": True},
    {"empresa": "AUSTRALIS", "correo": "soporte.australis@innovex.cl", "activo": True},
    {"empresa": "MULTI-X", "correo": "soporte.multix@innovex.cl", "activo": True},
    {"empresa": "SALMONES AUSTRAL", "correo": "soporte.salmonesaustral@innovex.cl", "activo": True},
    {"empresa": "YADRAN", "correo": "soporte.yadran@innovex.cl", "activo": True},
    {"empresa": "CAMANCHACA", "correo": "soporte.camanchaca@innovex.cl", "activo": True},
    {"empresa": "MARINE FARM", "correo": "soporte.marinefarm@innovex.cl", "activo": True},
    {"empresa": "VENTISQUEROS", "correo": "soporte.ventisqueros@innovex.cl", "activo": True},
    {"empresa": "COOKE AQUACULTURE", "correo": "soporte.cooke@innovex.cl", "activo": True},
    {"empresa": "INVERMAR", "correo": "soporte.invermar@innovex.cl", "activo": True},
]


class PortalService:
    """
    Servicio centralizado para funcionalidades del Portal de Soporte Innovex con persistencia SQLite.
    """

    # -------------------------------------------------------------
    # BITÁCORA / PIZARRA DE TURNO
    # -------------------------------------------------------------
    @classmethod
    def obtener_bitacora(cls) -> dict:
        try:
            bitacora = Bitacora.objects.first()
            if not bitacora:
                bitacora = Bitacora.objects.create(
                    texto="📝 Bienvenido a la Pizarra de Turno de Innovex Soporte.\n- Registre aquí novedades, pendientes y handover entre turnos."
                )
            return bitacora.to_dict()
        except Exception:
            return {
                "texto": "",
                "actualizado_en": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            }

    @classmethod
    def actualizar_bitacora(cls, texto: str) -> dict:
        try:
            bitacora = Bitacora.objects.first()
            if not bitacora:
                bitacora = Bitacora.objects.create(texto=texto or "")
            else:
                bitacora.texto = texto or ""
                bitacora.save()
            return {"status": "ok", "actualizado_en": bitacora.actualizado_en.strftime("%d/%m/%Y %H:%M")}
        except Exception as exc:
            return {"status": "error", "mensaje": str(exc)}

    # -------------------------------------------------------------
    # ASISTENTES DE TURNO
    # -------------------------------------------------------------
    @classmethod
    def obtener_asistentes(cls) -> list[dict]:
        try:
            if not Asistente.objects.exists():
                for a in ASISTENTES_DEFAULT:
                    Asistente.objects.create(**a)
            return [a.to_dict() for a in Asistente.objects.filter(activo=True).order_by("orden", "id")]
        except Exception:
            return [{"id": i+1, **a} for i, a in enumerate(ASISTENTES_DEFAULT)]

    # -------------------------------------------------------------
    # DESTINATARIOS Y EMPRESAS (GESTOR DE CORREOS)
    # -------------------------------------------------------------
    @classmethod
    def obtener_destinatarios(cls) -> list[dict]:
        try:
            if not Destinatario.objects.exists():
                for d in DESTINATARIOS_DEFAULT:
                    Destinatario.objects.create(**d)
            return [d.to_dict() for d in Destinatario.objects.all().order_by("empresa", "correo")]
        except Exception:
            return [{"id": i+1, **d} for i, d in enumerate(DESTINATARIOS_DEFAULT)]

    @classmethod
    def toggle_destinatario(cls, dest_id: int, activo: bool) -> dict:
        try:
            dest = Destinatario.objects.filter(id=dest_id).first()
            if dest:
                dest.activo = bool(activo)
                dest.save()
            return {"status": "ok"}
        except Exception as exc:
            return {"status": "error", "mensaje": str(exc)}

    @classmethod
    def crear_destinatario(cls, empresa: str, correo: str) -> dict:
        try:
            nuevo = Destinatario.objects.create(
                empresa=empresa.strip().upper(),
                correo=correo.strip().lower(),
                activo=True,
            )
            return {"status": "ok", "destinatario": nuevo.to_dict()}
        except Exception as exc:
            return {"status": "error", "mensaje": str(exc)}

    @classmethod
    def eliminar_destinatario(cls, dest_id: int) -> dict:
        try:
            Destinatario.objects.filter(id=dest_id).delete()
            return {"status": "ok"}
        except Exception as exc:
            return {"status": "error", "mensaje": str(exc)}

    # -------------------------------------------------------------
    # GENERADOR DE CORREO MASIVO DE FIN DE SEMANA
    # -------------------------------------------------------------
    @classmethod
    def calcular_fechas_fin_semana_actual(cls) -> tuple[str, str, int]:
        hoy = datetime.date.today()
        # Sábado más próximo
        dias_hasta_sabado = (5 - hoy.weekday()) % 7
        if dias_hasta_sabado == 0 and hoy.weekday() != 5:
            dias_hasta_sabado = 7
        sabado = hoy + datetime.timedelta(days=dias_hasta_sabado)
        domingo = sabado + datetime.timedelta(days=1)
        semana_iso = sabado.isocalendar()[1]
        return sabado.strftime("%d/%m/%Y"), domingo.strftime("%d/%m/%Y"), semana_iso

    @staticmethod
    def _format_fecha_corta(fecha_str: str) -> str:
        if not fecha_str:
            return ""
        try:
            dt = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            return dt.strftime("%d/%m")
        except ValueError:
            pass
        try:
            dt = datetime.datetime.strptime(fecha_str, "%d/%m/%Y")
            return dt.strftime("%d/%m")
        except ValueError:
            pass
        return fecha_str

    @classmethod
    def obtener_cargo_calculado(cls, nombre: str, cargo_base: str = "ASISTENTE DE SOPORTE") -> str:
        if not nombre:
            return cargo_base
        n = nombre.lower()
        if "hector" in n or "héctor" in n or "leonidas" in n:
            return "Asistente de Soporte Senior"
        elif any(k in n for k in ["leonardo", "gabriel", "felipe", "edwin"]):
            return "Asistente de Soporte Intermedio"
        elif "ivan" in n or "iván" in n:
            return "Asistente de Soporte"
        return cargo_base or "Asistente de Soporte"

    @classmethod
    def generar_html_correo_fin_semana(cls, personal: dict, fecha_sabado: str, fecha_domingo: str) -> str:
        nombre = personal.get("nombre", "Asistente de Soporte")
        cargo_base = personal.get("cargo", "ASISTENTE DE SOPORTE")
        cargo_calc = cls.obtener_cargo_calculado(nombre, cargo_base)
        sab_fmt = cls._format_fecha_corta(fecha_sabado)
        dom_fmt = cls._format_fecha_corta(fecha_domingo)

        return render_to_string(
            "emails/turno_fin_semana.html",
            {
                "fecha_sabado": sab_fmt,
                "fecha_domingo": dom_fmt,
                "personal": {
                    "nombre": nombre,
                    "telefono": personal.get("telefono", "+56 9 8419 4843"),
                    "correo": personal.get("correo", "soporte@innovex.cl"),
                    "cargo_calculado": cargo_calc,
                },
                "cargo_calculado": cargo_calc,
            },
        )

    @classmethod
    def enviar_correos_masivos(
        cls,
        semana: str | int | None,
        personal_id: int | str | None,
        fecha_sabado: str,
        fecha_domingo: str,
        correo_prueba: str = "",
    ) -> dict:
        sab_fmt = cls._format_fecha_corta(fecha_sabado)
        dom_fmt = cls._format_fecha_corta(fecha_domingo)
        sem_str = str(semana) if semana else str(datetime.date.today().isocalendar()[1])

        asistente_obj = None
        if personal_id:
            try:
                asistente_obj = Asistente.objects.filter(id=personal_id).first()
            except Exception:
                pass

        if asistente_obj:
            nombre_asistente = asistente_obj.nombre
            telefono_asistente = asistente_obj.telefono
            correo_asistente = asistente_obj.correo
            cargo_base = asistente_obj.cargo
        else:
            asistentes = cls.obtener_asistentes()
            if asistentes:
                a0 = asistentes[0]
                nombre_asistente = a0.get("nombre", "Asistente de Soporte")
                telefono_asistente = a0.get("telefono", "+56 9 8419 4843")
                correo_asistente = a0.get("correo", "soporte@innovex.cl")
                cargo_base = a0.get("cargo", "ASISTENTE DE SOPORTE")
            else:
                nombre_asistente = "Asistente de Soporte"
                telefono_asistente = "+56 9 8419 4843"
                correo_asistente = "soporte@innovex.cl"
                cargo_base = "ASISTENTE DE SOPORTE"

        cargo_calc = cls.obtener_cargo_calculado(nombre_asistente, cargo_base)

        personal_ctx = {
            "nombre": nombre_asistente,
            "telefono": telefono_asistente,
            "correo": correo_asistente,
            "cargo_calculado": cargo_calc,
        }

        html_content = render_to_string(
            "emails/turno_fin_semana.html",
            {
                "fecha_sabado": sab_fmt,
                "fecha_domingo": dom_fmt,
                "personal": personal_ctx,
                "cargo_calculado": cargo_calc,
            },
        )
        text_content = strip_tags(html_content)

        try:
            with open("test_correo_generado.html", "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception:
            pass

        nombre_parts = nombre_asistente.lower().split()
        if len(nombre_parts) >= 2:
            correo_remitente = f"{nombre_parts[0]}.{nombre_parts[1]}@innovex.cl"
        elif len(nombre_parts) == 1:
            correo_remitente = f"{nombre_parts[0]}@innovex.cl"
        else:
            correo_remitente = "soporte@innovex.cl"

        subject = f"ASISTENCIA SOPORTE INNOVEX FIN DE SEMANA - SEMANA {sem_str}"

        correo_prueba_clean = correo_prueba.strip()
        emails_enviados = 0

        if correo_prueba_clean:
            destinatarios = [c.strip() for c in correo_prueba_clean.replace(";", ",").split(",") if c.strip()]
            cc_list = []

            if destinatarios:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=correo_remitente,
                    to=destinatarios,
                    cc=cc_list,
                    reply_to=[correo_remitente],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                emails_enviados += 1
            mensaje = f"Se envió el correo masivo en MODO PRUEBA a {', '.join(destinatarios)}. Previsualización guardada en 'test_correo_generado.html'."
        else:
            destinatarios_qs = Destinatario.objects.filter(activo=True)
            empresas_map = {}
            for d in destinatarios_qs:
                emp = d.empresa.strip().upper()
                if emp not in empresas_map:
                    empresas_map[emp] = []
                if d.correo and d.correo.strip():
                    empresas_map[emp].append(d.correo.strip())

            cc_list = ["soporte@innovex.cl", "jefe.area@innovex.cl"]

            for emp_nombre, dests in empresas_map.items():
                if not dests:
                    continue
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=correo_remitente,
                    to=dests,
                    cc=cc_list,
                    reply_to=[correo_remitente],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                emails_enviados += 1

            mensaje = f"Se enviaron correos masivos a {emails_enviados} empresas agrupadas. Puedes previsualizar el HTML generado en el archivo 'test_correo_generado.html'."

        return {
            "status": "ok",
            "mensaje": mensaje,
            "emails_enviados": emails_enviados,
            "html_correo": html_content,
            "modo_prueba": bool(correo_prueba_clean),
        }


    # -------------------------------------------------------------
    # BUSCADOR & ÍNDICE TRAC WIKI
    # -------------------------------------------------------------
    @staticmethod
    def _quitar_tildes(texto: str) -> str:
        import unicodedata
        return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn').lower()

    @classmethod
    def buscar_trac_wiki(cls, query: str) -> dict:
        if not query or len(query.strip()) < 2:
            return {"results": []}

        # Procedimientos y manuales frecuentes de Innovex
        procedimientos = [
            {"title": "Manual de Configuración de Antenas Pancoordinator Jennic", "link": "https://intranet.innovex.cl/operaciones/wiki/PancoordinatorConfig", "snippet": "Guía de canales, PAN ID, comandos cmd status y cmd motes."},
            {"title": "Protocolo de Instalación y Calibración de Sensores de Oxígeno OXY", "link": "https://intranet.innovex.cl/operaciones/wiki/InstalacionOxigeno", "snippet": "Calibración al 100%, cambio de membrana y verificación de tramas :OXY."},
            {"title": "Configuración de Cámaras IP Domo y Enlaces PoE", "link": "https://intranet.innovex.cl/operaciones/wiki/CamarasIP", "snippet": "Asignación de IP fija 192.168.8.40 y revisión de switch PoE."},
            {"title": "Configuración de Red VPN tun0 y Acceso Remoto SSH", "link": "https://intranet.innovex.cl/operaciones/wiki/VPN_tun0", "snippet": "Diagnóstico de interfaz tun0, enrutamiento y servicio SSH innovex."},
            {"title": "Manual de Estación Meteorológica Davis Vantage Pro", "link": "https://intranet.innovex.cl/operaciones/wiki/EstacionDavis", "snippet": "Paquetería weather-station-davis y lectura de anemómetro/sensores climáticos."},
            {"title": "Mantenimiento y Reparación de Sensores de Salinidad COND", "link": "https://intranet.innovex.cl/operaciones/wiki/SensoresSalinidad", "snippet": "Limpieza de electrodos y verificación de conductividad en PSU."},
            {"title": "Protocolo de Ingreso de Técnico a Centro de Cultivo", "link": "https://intranet.innovex.cl/operaciones/wiki/ProtocoloIngresoTecnico", "snippet": "Lista de chequeo de bolsos, repuestos y evidencias fotográficas."},
            {"title": "Procedimiento de Cambio de Pilas y Verificación de Voltaje", "link": "https://intranet.innovex.cl/operaciones/wiki/VoltajesPilas", "snippet": "Umbrales mínimos de 3.0V y cambio preventivo en terreno."},
        ]

        q_norm = cls._quitar_tildes(query)
        coincidencias = []
        for p in procedimientos:
            t_norm = cls._quitar_tildes(p["title"])
            s_norm = cls._quitar_tildes(p["snippet"])
            if q_norm in t_norm or q_norm in s_norm:
                coincidencias.append(p)

        return {"results": coincidencias}

    @classmethod
    def obtener_indice_trac_wiki(cls) -> dict:
        indice = {
            "ANTENAS Y COMUNICACIÓN": [
                {"titulo": "Pancoordinator Jennic v2", "url": "https://intranet.innovex.cl/operaciones/wiki/Pancoordinator"},
                {"titulo": "Configuración de Red VPN tun0", "url": "https://intranet.innovex.cl/operaciones/wiki/VPN"},
                {"titulo": "Diagnóstico de Señal RF Motes", "url": "https://intranet.innovex.cl/operaciones/wiki/SenalRF"},
            ],
            "SENSORES Y CALIBRACIÓN": [
                {"titulo": "Sensores de Oxígeno (OXY)", "url": "https://intranet.innovex.cl/operaciones/wiki/OXY"},
                {"titulo": "Sensores de Salinidad (COND)", "url": "https://intranet.innovex.cl/operaciones/wiki/COND"},
                {"titulo": "Sensores de Corrientes (FLOW)", "url": "https://intranet.innovex.cl/operaciones/wiki/FLOW"},
            ],
            "CÁMARAS Y METEOROLOGÍA": [
                {"titulo": "Cámaras Domo IP y PoE", "url": "https://intranet.innovex.cl/operaciones/wiki/Camaras"},
                {"titulo": "Estación Davis Vantage Pro", "url": "https://intranet.innovex.cl/operaciones/wiki/Davis"},
            ],
            "PROCEDIMIENTOS DE TERRENO": [
                {"titulo": "Certificado de Instalación", "url": "https://intranet.innovex.cl/operaciones/wiki/Certificados"},
                {"titulo": "Ingreso Técnico y Repuestos", "url": "https://intranet.innovex.cl/operaciones/wiki/IngresoTecnico"},
                {"titulo": "Fallas MAM y Reemplazos", "url": "https://intranet.innovex.cl/operaciones/wiki/FallasMAM"},
            ]
        }
        return {"indice": indice}

    # -------------------------------------------------------------
    # ENCARGADOS DE ÁREA, ZONAS GEOGRÁFICAS Y TÉCNICOS
    # -------------------------------------------------------------
    @classmethod
    def _asegurar_estructura_personal(cls):
        from apps.core.constants.personal import ESTRUCTURA_ENCARGADOS
        if not EncargadoArea.objects.exists():
            for idx, (nombre_enc, data) in enumerate(ESTRUCTURA_ENCARGADOS.items(), start=1):
                enc, _ = EncargadoArea.objects.get_or_create(
                    nombre=nombre_enc,
                    defaults={"orden": idx, "activo": True}
                )
                for z_idx, zona in enumerate(data.get("zonas", []), start=1):
                    ZonaGeografica.objects.get_or_create(
                        nombre=zona,
                        defaults={"encargado_principal": enc, "orden": z_idx, "activo": True}
                    )
                for t_idx, tec in enumerate(data.get("tecnicos", []), start=1):
                    Tecnico.objects.get_or_create(
                        nombre=tec,
                        defaults={"encargado_principal": enc, "orden": t_idx, "activo": True}
                    )

    @classmethod
    def obtener_estructura_personal(cls) -> dict:
        try:
            cls._asegurar_estructura_personal()
            encargados_qs = EncargadoArea.objects.filter(activo=True).order_by("orden", "nombre")
            zonas_qs = ZonaGeografica.objects.filter(activo=True).order_by("orden", "nombre")
            tecnicos_qs = Tecnico.objects.filter(activo=True).order_by("orden", "nombre")

            mapa = {}
            for enc in encargados_qs:
                mapa[enc.nombre] = {
                    "zonas": list(enc.zonas.filter(activo=True).order_by("orden", "nombre").values_list("nombre", flat=True)),
                    "tecnicos": list(enc.tecnicos.filter(activo=True).order_by("orden", "nombre").values_list("nombre", flat=True)),
                }

            return {
                "status": "ok",
                "encargados": [enc.nombre for enc in encargados_qs],
                "todas_las_zonas": list(zonas_qs.values_list("nombre", flat=True)),
                "todos_los_tecnicos": list(tecnicos_qs.values_list("nombre", flat=True)),
                "mapa_completo": mapa,
            }
        except Exception:
            from apps.core.constants.personal import ESTRUCTURA_ENCARGADOS, TODAS_LAS_ZONAS, TODOS_LOS_TECNICOS
            return {
                "status": "ok",
                "encargados": list(ESTRUCTURA_ENCARGADOS.keys()),
                "todas_las_zonas": TODAS_LAS_ZONAS,
                "todos_los_tecnicos": TODOS_LOS_TECNICOS,
                "mapa_completo": ESTRUCTURA_ENCARGADOS,
            }
