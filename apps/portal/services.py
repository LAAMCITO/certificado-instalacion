"""
Service centralizado para el Portal de Soporte Innovex (Django ORM + SQLite).
"""

import datetime
import base64
import re
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from pathlib import Path
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import (
    Empresa, Asistente, Destinatario, Bitacora, EncargadoArea,
    ZonaGeografica, Tecnico, CentroContactoTicket, HistorialTicketEnviado
)


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
DESTINATARIOS_DEFAULT = []


class CustomEmailMessage(EmailMessage):
    """Wrapper para despachar estructuras MIME personalizadas (related/mixed) vía Django."""
    def __init__(self, mime_obj, to_list, cc_list=None, from_email=None, reply_to=None):
        super().__init__(
            subject=mime_obj.get("Subject", ""),
            from_email=from_email or mime_obj.get("From", ""),
            to=to_list,
            cc=cc_list or [],
            reply_to=reply_to or []
        )
        self._mime_obj = mime_obj

    def message(self, policy=None):
        if policy is not None:
            self._mime_obj.policy = policy
        return self._mime_obj


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
    def normalizar_nombre_empresa(cls, empresa: str) -> str:
        if not empresa:
            return ""
        emp_clean = empresa.strip()
        if not emp_clean:
            return ""

        from apps.core.constants.empresas import EMPRESAS
        for emp_std in EMPRESAS:
            if emp_std.lower() == emp_clean.lower():
                return emp_std

        existentes = Destinatario.objects.filter(empresa__iexact=emp_clean)
        for ex in existentes:
            if not ex.empresa.isupper():
                return ex.empresa

        if emp_clean.isupper():
            return emp_clean.title()

        return emp_clean

    @classmethod
    def obtener_destinatarios(cls) -> list[dict]:
        try:
            if not Destinatario.objects.exists():
                for d in DESTINATARIOS_DEFAULT:
                    d_copy = dict(d)
                    d_copy["empresa"] = cls.normalizar_nombre_empresa(d_copy["empresa"])
                    Destinatario.objects.create(**d_copy)

            # Normalizar cualquier registro existente en la BD que haya quedado guardado en ALL-CAPS (e.g. legacy BLUMAR)
            destinatarios_qs = Destinatario.objects.all().order_by("empresa", "correo")
            resultado = []
            for d in destinatarios_qs:
                norm = cls.normalizar_nombre_empresa(d.empresa)
                if norm != d.empresa:
                    d.empresa = norm
                    d.save()
                resultado.append(d.to_dict())

            return resultado
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
            empresa_clean = cls.normalizar_nombre_empresa(empresa)
            nuevo = Destinatario.objects.create(
                empresa=empresa_clean,
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
            correo_asistente = "soporte@innovex.cl"
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
                emp = cls.normalizar_nombre_empresa(d.empresa)
                if emp not in empresas_map:
                    empresas_map[emp] = []
                if d.correo and d.correo.strip() and "@" in d.correo:
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

    # -------------------------------------------------------------
    # MÓDULOS DE COMUNICACIONES: TICKETS DE FALLA
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # GESTIÓN DE CENTROS & CONTACTOS DE TICKETS
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # GESTIÓN DE CENTROS & CONTACTOS DE TICKETS
    # -------------------------------------------------------------
    EMPRESAS_CANONICAS = [
        "Abick", "AquaChile", "AquaGen", "Australis", "Blumar", "Caleta Bay", "Camanchaca", "Cermaq",
        "Cooke Aquaculture", "Invermar", "Marine Farm", "Mowi", "Multi-X", "NovaAustral",
        "Salmones Austral", "Salmones Aysen", "Salmones de Chile", "SurProceso", "Ventisqueros", "Yadran"
    ]

    @classmethod
    def _asegurar_empresas(cls):
        """Asegura la creación inicial de las empresas canónicas y vinculación de Destinatarios."""
        for nom in cls.EMPRESAS_CANONICAS:
            Empresa.objects.get_or_create(nombre=nom, defaults={"activo": True})

        # Vincular Destinatarios existentes a su entidad Empresa sin eliminar jamás registros
        for d in Destinatario.objects.filter(empresa_rel__isnull=True):
            emp_nom = d.empresa.strip()
            if not emp_nom:
                continue
            emp_match = Empresa.objects.filter(nombre__iexact=emp_nom).first()
            if not emp_match:
                emp_match, _ = Empresa.objects.get_or_create(nombre=emp_nom, defaults={"activo": True})
            d.empresa = emp_match.nombre
            d.empresa_rel = emp_match
            d.save(update_fields=["empresa", "empresa_rel"])

    @classmethod
    def obtener_empresas(cls) -> list[dict]:
        cls._asegurar_empresas()
        qs = Empresa.objects.filter(activo=True).order_by("nombre")
        return [e.to_dict() for e in qs]

    @classmethod
    def _asegurar_centros_tickets(cls):
        """Asegura centros iniciales de Cermaq únicamente si no existen en la BD."""
        cls._asegurar_estructura_personal()
        cls._asegurar_empresas()

        # Si ya existen centros de Cermaq registrados en la BD, respetamos fielmente las modificaciones y eliminaciones del usuario
        if CentroContactoTicket.objects.filter(empresa="Cermaq").exists():
            return

        # Asegurar zona Puluqui en ZonaGeografica
        manuel = EncargadoArea.objects.filter(nombre__icontains="Manuel").first()
        ZonaGeografica.objects.get_or_create(
            nombre="Puluqui",
            defaults={"encargado_principal": manuel, "activo": True, "orden": 6}
        )

        mapeo_zonas_db = {
            "Puerto Montt": "Pto. Montt",
            "Chiloé": "Chiloé",
            "Puerto Cisnes": "Pto. Cisnes",
            "Punta Arenas": "Pta. Arenas (PUQ)",
            "Ayacara": "Ayacara",
            "Calbuco": "Calbuco",
            "Chacabuco": "Pto. Chacabuco",
            "Puerto Chacabuco": "Pto. Chacabuco",
            "Puluqui": "Puluqui",
        }

        areas_correos_cermaq = {
            "Punta Arenas": "raul.rivera@cermaq.com, william.toro@cermaq.com, paulino.morales@cermaq.com, central.monitoreo@cermaq.com",
            "Puerto Chacabuco": "alvaro.quintana@cermaq.com, william.toro@cermaq.com, paulino.morales@cermaq.com, central.monitoreo@cermaq.com",
            "Chacabuco": "alvaro.quintana@cermaq.com, william.toro@cermaq.com, paulino.morales@cermaq.com, central.monitoreo@cermaq.com",
            "Puerto Cisnes": "william.toro@cermaq.com, paulino.morales@cermaq.com, central.monitoreo@cermaq.com",
            "Ayacara": "javier.olave@cermaq.com, william.toro@cermaq.com, paulino.morales@cermaq.com, central.monitoreo@cermaq.com",
            "Calbuco": "gonzalo.saavedra@cermaq.com, william.toro@cermaq.com, paulino.morales@cermaq.com, central.monitoreo@cermaq.com",
            "Chiloé": "osvaldo.diazdiaz@cermaq.com, victor.aguilar.ojeda@cermaq.com, william.toro@cermaq.com, paulino.morales@cermaq.com, central.monitoreo@cermaq.com",
            "Puerto Montt": "antonio.miranda@cermaq.com, william.toro@cermaq.com, paulino.morales@cermaq.com, central.monitoreo@cermaq.com",
            "Puluqui": "gonzalo.saavedra@cermaq.com, william.toro@cermaq.com, paulino.morales@cermaq.com, central.monitoreo@cermaq.com",
        }

        # Catálogo maestro de monitores Cermaq con correo de centro y área
        cermaq_monitores = [
            ("Acopio Chinquihue", "marco.almonacid@cermaq.com, supervisor.acopio.aisc@cermaq.com, antonio.miranda@cermaq.com", "Puerto Montt", True),
            ("Acopio Quemchi", "acopioquemchi@cermaq.com", "Chiloé", True),
            ("Aguantao", "aguantao@cermaq.com", "Chiloé", False),
            ("Aldunate", "centro.aldunate@cermaq.com", "Puerto Cisnes", False),
            ("Aulen", "centro.aulen@cermaq.com", "Puerto Montt", True),
            ("Bertrand", "centro.bertrand@cermaq.com", "Punta Arenas", True),
            ("Buill", "centro.buill@cermaq.com", "Ayacara", True),
            ("Cachihue", "centro.cachihue@cermaq.com", "Chiloé", True),
            ("Calen 1", "calen1@cermaq.com", "Chiloé", True),
            ("Calen 2", "calen2@cermaq.com", "Chiloé", True),
            ("Chauco", "centro.chauco@cermaq.com", "Chiloé", True),
            ("Caleta Soledad", "caleta.soledad@cermaq.com", "Puerto Montt", False),
            ("Chaullin Norte", "centro.chaullinnorte@cermaq.com", "Chiloé", True),
            ("Chaullin Weste", "chaullinweste@cermaq.com", "Chiloé", True),
            ("Chidhuapi 1", "centro.chidhuapi1@cermaq.com", "Calbuco", True),
            ("Chidhuapi 2", "chidhuapi2@cermaq.com", "Calbuco", True),
            ("Chidhuapi 3", "centro.chidhuapi3@cermaq.com", "Calbuco", True),
            ("Chidhuapi 4", "centro.chidhuapi4@cermaq.com", "Calbuco", True),
            ("Churrecue", "centro.churrecue@cermaq.com", "Chacabuco", True),
            ("Colaco 4", "colaco4@cermaq.com", "Calbuco", False),
            ("Colaco 4 200", "", "Calbuco", False),
            ("Darsena Norte", "centro.darsenanorte@cermaq.com", "Punta Arenas", False),
            ("Ducañas", "centro.ducanas@cermaq.com", "Chiloé", True),
            ("Estero", "centro.estero@cermaq.com", "Punta Arenas", True),
            ("Desembocadura", "centro.desembocadura@cermaq.com", "Punta Arenas", False),
            ("Estero Conche", "centro.esteroconche@cermaq.com", "Puerto Cisnes", False),
            ("Furia", "centro.furia@cermaq.com", "Punta Arenas", False),
            ("Imelev", "imelev@cermaq.com", "Punta Arenas", False),
            ("Isla García", "centro.islagarcia@cermaq.com", "Punta Arenas", True),
            ("Isla Guzman", "centro.islaguzman@cermaq.com", "Punta Arenas", False),
            ("Isla Juan", "centro.islajuan@cermaq.com", "Punta Arenas", False),
            ("Isla Tac", "centro.islatac@cermaq.com", "Chiloé", True),
            ("Linguar", "centro.linguar@cermaq.com", "Puerto Montt", True),
            ("Linlinao", "linlinao@cermaq.com", "Chiloé", False),
            ("Llancacheo", "llancacheo@cermaq.com", "Puluqui", True),
            ("Luchin", "centro.luchin@cermaq.com", "Chacabuco", True),
            ("Macetero", "centro.macetero@cermaq.com", "Puerto Cisnes", False),
            ("Malomacum", "centro.malomacum@cermaq.com", "Puerto Montt", True),
            ("Manzano", "centro.manzano@cermaq.com", "Puerto Montt", True),
            ("Navarro", "navarro@cermaq.com", "Punta Arenas", True),
            ("Matilde", "centro.matilde@cermaq.com", "Chacabuco", False),
            ("Pollollo", "centro.pollollo@cermaq.com", "Puerto Montt", True),
            ("Punta Darsena", "punta.darsena@cermaq.com", "Punta Arenas", False),
            ("Punta Gruesa", "centro.puntagruesa@cermaq.com", "Ayacara", False),
            ("Punta Laura", "puntalaura@cermaq.com", "Punta Arenas", True),
            ("Punta Isla", "centro.puntaisla@cermaq.com", "Chacabuco", False),
            ("Punta Quintana", "centro.puntaquintana@cermaq.com", "Chacabuco", False),
            ("Punta Victoria", "centro.puntavictoria@cermac.com", "Chacabuco", False),
            ("Quilen", "quilen@cermaq.com", "Chiloé", True),
            ("Quilen Replica (base tierra)", "", "Chiloé", True),
            ("Reñihue", "centro.renihue@cermaq.com", "Ayacara", True),
            ("Sureste", "sureste@cermaq.com", "Puluqui", True),
            ("Tranqui 1", "centro.tranqui1@cermaq.com", "Chiloé", True),
            ("Tranqui 2", "centro.tranqui2@cermaq.com", "Chiloé", True),
            ("Transito", "centro.transito@cermaq.com", "Chacabuco", False),
            ("Tubildad", "centro.tubildad@cermaq.com", "Chiloé", False),
            ("Unicornio", "unicornio@cermaq.com", "Punta Arenas", False),
            ("Unicornio Sur", "unicorniosur@cermaq.com", "Punta Arenas", True),
            ("Voigue", "centro.voigue@cermaq.com", "Chiloé", True),
            ("Vilupulli", "centro.vilupulli@cermaq.com", "Chiloé", False),
            ("Yelcho", "yelcho@cermaq.com", "Chiloé", True),
            ("Yoye", "yoye@cermaq.com", "Chiloé", True),
            ("Zañartu", "centro.zanartu@cermaq.com", "Puerto Cisnes", False),
        ]

        emp_cermaq = Empresa.objects.filter(nombre="Cermaq").first()

        for monitor, correo_centro, area, activo in cermaq_monitores:
            zona_db = mapeo_zonas_db.get(area, area)
            zona_obj = ZonaGeografica.objects.filter(nombre=zona_db).first() or ZonaGeografica.objects.filter(nombre__icontains=area).first()
            correos_area = areas_correos_cermaq.get(area, "william.toro@cermaq.com, paulino.morales@cermaq.com, central.monitoreo@cermaq.com")
            correos_cc = f"{correos_area}, soporte@innovex.cl, jefe.area@innovex.cl"

            CentroContactoTicket.objects.create(
                empresa="Cermaq",
                nombre_centro=monitor,
                empresa_rel=emp_cermaq,
                zona_geografica=zona_obj,
                destinatarios_to=correo_centro,
                destinatarios_cc=correos_cc,
                activo=activo,
            )

    @classmethod
    def obtener_centros_tickets(cls, incluir_inactivos: bool = False) -> list[dict]:
        cls._asegurar_centros_tickets()
        if incluir_inactivos:
            qs = CentroContactoTicket.objects.all().select_related("zona_geografica", "empresa_rel").order_by("empresa", "nombre_centro")
        else:
            qs = CentroContactoTicket.objects.filter(activo=True).select_related("zona_geografica", "empresa_rel").order_by("empresa", "nombre_centro")
        return [c.to_dict() for c in qs]

    @classmethod
    def guardar_centro_ticket(cls, datos: dict) -> dict:
        cid = datos.get("id")
        empresa_raw = (datos.get("empresa") or "").strip()
        emp_match = Empresa.objects.filter(nombre__iexact=empresa_raw).first()
        empresa = emp_match.nombre if emp_match else empresa_raw
        nombre_centro = (datos.get("nombre_centro") or "").strip()
        codigo_location = (datos.get("codigo_location") or "").strip()
        zona_id = datos.get("zona_id")
        dest_to = (datos.get("destinatarios_to") or "").strip()
        dest_cc = (datos.get("destinatarios_cc") or "").strip()
        activo = bool(datos.get("activo", True))

        if not empresa or not nombre_centro:
            raise ValueError("Empresa y Nombre del Centro son obligatorios.")

        zona_obj = ZonaGeografica.objects.filter(id=zona_id).first() if zona_id else None

        if cid:
            obj = CentroContactoTicket.objects.filter(id=cid).first()
            if not obj:
                raise ValueError(f"Centro con id {cid} no encontrado.")
            obj.empresa = empresa
            obj.empresa_rel = emp_match
            obj.nombre_centro = nombre_centro
            obj.codigo_location = codigo_location
            obj.zona_geografica = zona_obj
            obj.destinatarios_to = dest_to
            obj.destinatarios_cc = dest_cc
            obj.activo = activo
            obj.save()
        else:
            obj = CentroContactoTicket.objects.create(
                empresa=empresa,
                empresa_rel=emp_match,
                nombre_centro=nombre_centro,
                codigo_location=codigo_location,
                zona_geografica=zona_obj,
                destinatarios_to=dest_to,
                destinatarios_cc=dest_cc,
                activo=activo
            )

        return {"status": "ok", "centro": obj.to_dict()}

    @classmethod
    def eliminar_centro_ticket(cls, centro_id: int) -> dict:
        obj = CentroContactoTicket.objects.filter(id=centro_id).first()
        if obj:
            obj.delete()
            return {"status": "ok", "mensaje": "Centro eliminado correctamente"}
        return {"status": "error", "mensaje": "Centro no encontrado"}

    @classmethod
    def _obtener_datos_personal(cls, personal_id: int | str | None = None) -> dict:
        asistente_obj = None
        if personal_id:
            try:
                asistente_obj = Asistente.objects.filter(id=personal_id).first()
            except Exception:
                pass

        if asistente_obj:
            nombre = asistente_obj.nombre
            cargo_base = asistente_obj.cargo
            telefono = asistente_obj.telefono
            correo = asistente_obj.correo
        else:
            asistentes = cls.obtener_asistentes()
            if asistentes:
                a0 = asistentes[0]
                nombre = a0.get("nombre", "Asistente de Soporte")
                cargo_base = a0.get("cargo", "ASISTENTE DE SOPORTE")
                telefono = a0.get("telefono", "(+56) 9 841 948 43")
                correo = a0.get("correo", "soporte@innovex.cl")
            else:
                nombre = "Asistente de Soporte"
                cargo_base = "ASISTENTE DE SOPORTE"
                telefono = "(+56) 9 841 948 43"
                correo = "soporte@innovex.cl"

        cargo_calc = cls.obtener_cargo_calculado(nombre, cargo_base)
        return {
            "nombre": nombre,
            "cargo": cargo_base,
            "cargo_calculado": cargo_calc,
            "telefono": telefono,
            "correo": correo,
        }

    @classmethod
    def generar_html_ticket(cls, tipo_ticket: str, datos: dict, personal: dict | None = None) -> tuple[str, str]:
        """
        Genera el asunto y el HTML del correo para el tipo de ticket especificado.
        Retorna (asunto, html_content).
        """
        if not personal:
            personal = cls._obtener_datos_personal(datos.get("personal_id"))

        centro_nombre = datos.get("nombre_centro") or datos.get("centro") or "Centro"
        empresa = datos.get("empresa") or ""

        ctx = {
            "centro_nombre": centro_nombre,
            "empresa": empresa,
            "personal": personal,
            "imagen_evidencia": datos.get("imagen_evidencia", ""),
            "imagen_grafica": datos.get("imagen_grafica", ""),
            "imagen_defectuoso": datos.get("imagen_defectuoso", ""),
            "imagen_repuesto": datos.get("imagen_repuesto", ""),
        }

        if tipo_ticket == "conexion":
            asunto = f"Ticket - {centro_nombre} / CONEXIÓN."
            template_name = "emails/ticket_conexion.html"

        elif tipo_ticket == "falla_equipo":
            numero_equipo = str(datos.get("numero_equipo", "")).strip()
            ubicacion = str(datos.get("ubicacion", "")).strip()
            numero_jaula = str(datos.get("numero_jaula", "")).strip()

            partes_equipo = []
            if numero_equipo:
                partes_equipo.append(numero_equipo)
            if ubicacion:
                partes_equipo.append(ubicacion)
            elif numero_jaula:
                partes_equipo.append(f"Jaula {numero_jaula}")

            eq_info = " ".join(partes_equipo)
            raw_ref = datos.get("texto_referencia")
            texto_referencia = raw_ref.strip() if (raw_ref and str(raw_ref).strip()) else "Corte de datos por posible falla en su funcionamiento."
            asunto = f"Ticket - {centro_nombre} - Falla de equipo {eq_info}".strip() if eq_info else f"Ticket - {centro_nombre} - Falla de equipo"
            ctx.update({
                "numero_equipo": numero_equipo,
                "numero_jaula": numero_jaula,
                "ubicacion": ubicacion,
                "eq_info": eq_info,
                "texto_referencia": texto_referencia,
                "es_corriente": bool(datos.get("es_corriente", False)),
            })
            template_name = "emails/ticket_falla_equipo.html"

        elif tipo_ticket == "falla_sensor":
            tipo_sensor_raw = str(datos.get("tipo_sensor", "oxigeno")).strip().lower()
            if "salin" in tipo_sensor_raw:
                tipo_sensor_key = "salinidad"
                tipo_sensor_display = "Salinidad"
            elif "integ" in tipo_sensor_raw:
                tipo_sensor_key = "integrado"
                tipo_sensor_display = "Integrado"
            else:
                tipo_sensor_key = "oxigeno"
                tipo_sensor_display = "Oxígeno"

            profundidad = str(datos.get("profundidad", "10")).strip()
            numero_jaula = str(datos.get("numero_jaula", "")).strip()
            ubicacion = str(datos.get("ubicacion", "")).strip()

            partes_sens = []
            if profundidad:
                partes_sens.append(f"{profundidad}m")
            if ubicacion:
                partes_sens.append(ubicacion)
            elif numero_jaula:
                partes_sens.append(f"Jaula {numero_jaula}")

            sens_info = " ".join(partes_sens)
            raw_ref = datos.get("texto_referencia")
            texto_referencia = raw_ref.strip() if (raw_ref and str(raw_ref).strip()) else "Corte de datos por posible falla en su funcionamiento."

            if sens_info:
                asunto = f"Ticket - {centro_nombre} - Falla sensor de {tipo_sensor_display} {sens_info}".strip()
            else:
                asunto = f"Ticket - {centro_nombre} - Falla sensor de {tipo_sensor_display}".strip()

            ctx.update({
                "tipo_sensor": tipo_sensor_display,
                "tipo_sensor_key": tipo_sensor_key,
                "tipo_sensor_display": tipo_sensor_display,
                "profundidad": profundidad,
                "numero_jaula": numero_jaula,
                "ubicacion": ubicacion,
                "sens_info": sens_info,
                "texto_referencia": texto_referencia,
            })
            template_name = "emails/ticket_falla_sensor.html"

        else:
            raise ValueError(f"Tipo de ticket desconocido: {tipo_ticket}")

        html_content = render_to_string(template_name, ctx)
        return asunto, html_content

    @classmethod
    def enviar_correo_ticket(
        cls,
        tipo_ticket: str,
        datos: dict,
        personal_id: int | str | None = None,
        destinatarios_to: str | list[str] = "",
        destinatarios_cc: str | list[str] = "",
        correo_prueba: str = "",
        adjuntar_guia: bool = True
    ) -> dict:
        personal = cls._obtener_datos_personal(personal_id)

        # Si es ticket de conexión, nunca se adjunta guía de mantención PDF
        if tipo_ticket == "conexion":
            adjuntar_guia = False

        # Parsear correos destinatarios
        def _parse_emails(raw):
            if isinstance(raw, list):
                return [c.strip() for c in raw if c and c.strip()]
            if not raw:
                return []
            return [c.strip() for c in re.split(r"[,;\n\r]+", str(raw)) if c and c.strip()]

        to_list = _parse_emails(destinatarios_to)
        cc_list = _parse_emails(destinatarios_cc)

        es_prueba = bool(correo_prueba and correo_prueba.strip())
        if es_prueba:
            to_list = _parse_emails(correo_prueba)
            cc_list = []

        if not to_list:
            raise ValueError("No se especificaron destinatarios válidos para el envío.")

        # Remitente
        nombre_parts = personal["nombre"].lower().split()
        if len(nombre_parts) >= 2:
            correo_remitente = f"{nombre_parts[0]}.{nombre_parts[1]}@innovex.cl"
        elif len(nombre_parts) == 1:
            correo_remitente = f"{nombre_parts[0]}@innovex.cl"
        else:
            correo_remitente = "soporte@innovex.cl"

        # Pre-procesar imágenes base64 a CIDs antes de renderizar para evitar líneas largas en el HTML
        inline_images = []
        datos_render = dict(datos)

        for img_key in ["imagen_evidencia", "imagen_grafica", "imagen_defectuoso", "imagen_repuesto"]:
            val = datos.get(img_key)
            if val and isinstance(val, str) and "base64," in val:
                try:
                    header, b64_str = val.split("base64,", 1)
                    sub_match = re.search(r"image/([a-zA-Z0-9+.-]+)", header, re.IGNORECASE)
                    img_type = sub_match.group(1).lower() if sub_match else "png"
                    if img_type == "jpg":
                        img_type = "jpeg"
                    clean_b64 = re.sub(r"[\s\r\n]+", "", b64_str)
                    img_bytes = base64.b64decode(clean_b64)
                    cid = f"img_{uuid.uuid4().hex[:10]}"
                    inline_images.append((img_bytes, img_type, cid))
                    datos_render[img_key] = f"cid:{cid}"
                except Exception:
                    datos_render[img_key] = ""

        asunto, html_content = cls.generar_html_ticket(tipo_ticket, datos_render, personal)
        text_content = strip_tags(html_content)

        # Respaldo de seguridad por si algún campo libre contenía data URIs adicionales
        def _sub_remaining(match):
            try:
                sub_type = match.group(1).lower()
                if sub_type == "jpg":
                    sub_type = "jpeg"
                clean_b64 = re.sub(r"[\s\r\n]+", "", match.group(2))
                img_bytes = base64.b64decode(clean_b64)
                cid = f"img_{uuid.uuid4().hex[:10]}"
                inline_images.append((img_bytes, sub_type, cid))
                return f'src="cid:{cid}"'
            except Exception:
                return 'src=""'

        html_final = re.sub(
            r'src=["\']data:image/([a-zA-Z0-9+.-]+);base64,([^"\']+)["\']',
            _sub_remaining,
            html_content,
            flags=re.IGNORECASE
        )

        # Construir estructura MIME estándar RFC 2387
        guias_dir = getattr(settings, "STORAGE_DIR", Path("storage")) / "guias"
        guia_path = guias_dir / "guia_mantenimiento_correctivo_innovex.pdf"
        tiene_adjunto_pdf = bool(adjuntar_guia and guia_path.exists() and guia_path.is_file())

        if tiene_adjunto_pdf:
            # Estructura: multipart/mixed -> [multipart/related (HTML + Inline Images), application/pdf]
            root_msg = MIMEMultipart("mixed")
            root_msg["Subject"] = asunto
            root_msg["From"] = correo_remitente
            root_msg["To"] = ", ".join(to_list)
            if cc_list:
                root_msg["Cc"] = ", ".join(cc_list)
            root_msg["Reply-To"] = f"{correo_remitente}, soporte@innovex.cl"

            related_part = MIMEMultipart("related")
            alt_part = MIMEMultipart("alternative")
            alt_part.attach(MIMEText(text_content, "plain", "utf-8"))
            alt_part.attach(MIMEText(html_final, "html", "utf-8"))
            related_part.attach(alt_part)

            for img_bytes, img_type, cid in inline_images:
                mime_img = MIMEImage(img_bytes, _subtype=img_type)
                mime_img.add_header("Content-ID", f"<{cid}>")
                mime_img.add_header("Content-Disposition", "inline", filename=f"{cid}.{img_type}")
                related_part.attach(mime_img)

            root_msg.attach(related_part)

            mime_pdf = MIMEApplication(guia_path.read_bytes(), _subtype="pdf")
            mime_pdf.add_header("Content-Disposition", "attachment", filename="Guia_Mantencion_Correctiva_Innovex.pdf")
            root_msg.attach(mime_pdf)

        else:
            # Estructura: multipart/related -> [multipart/alternative (text + HTML), inline images]
            root_msg = MIMEMultipart("related")
            root_msg["Subject"] = asunto
            root_msg["From"] = correo_remitente
            root_msg["To"] = ", ".join(to_list)
            if cc_list:
                root_msg["Cc"] = ", ".join(cc_list)
            root_msg["Reply-To"] = f"{correo_remitente}, soporte@innovex.cl"

            alt_part = MIMEMultipart("alternative")
            alt_part.attach(MIMEText(text_content, "plain", "utf-8"))
            alt_part.attach(MIMEText(html_final, "html", "utf-8"))
            root_msg.attach(alt_part)

            for img_bytes, img_type, cid in inline_images:
                mime_img = MIMEImage(img_bytes, _subtype=img_type)
                mime_img.add_header("Content-ID", f"<{cid}>")
                mime_img.add_header("Content-Disposition", "inline", filename=f"{cid}.{img_type}")
                root_msg.attach(mime_img)

        # Enviar correo con CustomEmailMessage para que Django maneje el backend configurado
        msg = CustomEmailMessage(
            root_msg,
            to_list=to_list,
            cc_list=cc_list,
            from_email=correo_remitente,
            reply_to=[correo_remitente, "soporte@innovex.cl"]
        )
        msg.send()

        # Guardar en Historial
        try:
            HistorialTicketEnviado.objects.create(
                tipo_ticket=tipo_ticket,
                empresa=datos.get("empresa", ""),
                centro=datos.get("nombre_centro") or datos.get("centro", ""),
                asunto=asunto,
                asistente_nombre=personal["nombre"],
                destinatarios_to=", ".join(to_list),
                destinatarios_cc=", ".join(cc_list),
                es_prueba=es_prueba,
                manual_adjunto=adjuntar_guia,
                datos_ticket=datos,
            )
        except Exception:
            pass

        modo_msg = " en MODO PRUEBA" if es_prueba else ""
        return {
            "status": "ok",
            "mensaje": f"Ticket enviado exitosamente{modo_msg} a {', '.join(to_list)}.",
            "asunto": asunto,
            "destinatarios": to_list,
            "cc": cc_list,
            "es_prueba": es_prueba,
        }

    @classmethod
    def obtener_historial_tickets(cls, limite: int = 30) -> list[dict]:
        qs = HistorialTicketEnviado.objects.all().order_by("-fecha_envio")[:limite]
        resultado = []
        for h in qs:
            resultado.append({
                "id": h.id,
                "tipo_ticket": h.tipo_ticket,
                "tipo_display": h.get_tipo_ticket_display(),
                "empresa": h.empresa,
                "centro": h.centro,
                "asunto": h.asunto,
                "asistente": h.asistente_nombre,
                "destinatarios_to": h.destinatarios_to,
                "destinatarios_cc": h.destinatarios_cc,
                "es_prueba": h.es_prueba,
                "manual_adjunto": h.manual_adjunto,
                "fecha_envio": h.fecha_envio.strftime("%d/%m/%Y %H:%M"),
            })
        return resultado

