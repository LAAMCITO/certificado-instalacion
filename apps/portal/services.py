"""
Service centralizado para el Portal de Soporte Innovex (Django ORM + SQLite).
"""

import datetime
import base64
import re
import uuid
from email.mime.image import MIMEImage
from pathlib import Path
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import (
    Asistente, Destinatario, Bitacora, EncargadoArea,
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

    # -------------------------------------------------------------
    # MÓDULOS DE COMUNICACIONES: TICKETS DE FALLA
    # -------------------------------------------------------------
    @classmethod
    def _asegurar_centros_tickets(cls):
        """Asegura centros iniciales de prueba/referencia para tickets si la tabla está vacía."""
        if not CentroContactoTicket.objects.exists():
            centros_seed = [
                {"empresa": "CERMAQ", "nombre_centro": "Chidhuapi 1", "codigo_location": "ch-chidhuapi1", "destinatarios_to": "jefe.centro.chidhuapi@cermaq.com", "destinatarios_cc": "soporte.cermaq@innovex.cl"},
                {"empresa": "CERMAQ", "nombre_centro": "Tranqui 1", "codigo_location": "ce-tranqui1", "destinatarios_to": "jefe.centro.tranqui@cermaq.com", "destinatarios_cc": "soporte.cermaq@innovex.cl"},
                {"empresa": "MOWI", "nombre_centro": "Isla Sánchez", "codigo_location": "mw-islasanchez", "destinatarios_to": "jefe.centro.islasanchez@mowi.com", "destinatarios_cc": "soporte.mowi@innovex.cl"},
                {"empresa": "CAMANCHACA", "nombre_centro": "Pollollo", "codigo_location": "ce-pollollo", "destinatarios_to": "jefe.centro.pollollo@camanchaca.cl", "destinatarios_cc": "soporte.camanchaca@innovex.cl"},
                {"empresa": "AQUACHILE", "nombre_centro": "Sa-Lleuna", "codigo_location": "sa-lleuna", "destinatarios_to": "jefe.centro.salleuna@aquachile.com", "destinatarios_cc": "soporte.aquachile@innovex.cl"},
                {"empresa": "BLUMAR", "nombre_centro": "Ahoni", "codigo_location": "ca-ahoni", "destinatarios_to": "jefe.centro.ahoni@blumar.com", "destinatarios_cc": "soporte.blumar@innovex.cl"},
            ]
            for item in centros_seed:
                CentroContactoTicket.objects.get_or_create(
                    empresa=item["empresa"],
                    nombre_centro=item["nombre_centro"],
                    defaults={
                        "codigo_location": item["codigo_location"],
                        "destinatarios_to": item["destinatarios_to"],
                        "destinatarios_cc": item["destinatarios_cc"],
                        "activo": True
                    }
                )

    @classmethod
    def obtener_centros_tickets(cls) -> list[dict]:
        cls._asegurar_centros_tickets()
        qs = CentroContactoTicket.objects.filter(activo=True).select_related("zona_geografica").order_by("empresa", "nombre_centro")
        return [c.to_dict() for c in qs]

    @classmethod
    def guardar_centro_ticket(cls, datos: dict) -> dict:
        cid = datos.get("id")
        empresa = (datos.get("empresa") or "").strip().upper()
        nombre_centro = (datos.get("nombre_centro") or "").strip()
        codigo_location = (datos.get("codigo_location") or "").strip()
        zona_id = datos.get("zona_id")
        dest_to = (datos.get("destinatarios_to") or "").strip()
        dest_cc = (datos.get("destinatarios_cc") or "").strip()

        if not empresa or not nombre_centro:
            raise ValueError("Empresa y Nombre del Centro son obligatorios.")

        zona_obj = ZonaGeografica.objects.filter(id=zona_id).first() if zona_id else None

        if cid:
            obj = CentroContactoTicket.objects.filter(id=cid).first()
            if not obj:
                raise ValueError(f"Centro con id {cid} no encontrado.")
            obj.empresa = empresa
            obj.nombre_centro = nombre_centro
            obj.codigo_location = codigo_location
            obj.zona_geografica = zona_obj
            obj.destinatarios_to = dest_to
            obj.destinatarios_cc = dest_cc
            obj.save()
        else:
            obj = CentroContactoTicket.objects.create(
                empresa=empresa,
                nombre_centro=nombre_centro,
                codigo_location=codigo_location,
                zona_geografica=zona_obj,
                destinatarios_to=dest_to,
                destinatarios_cc=dest_cc,
                activo=True
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
            numero_equipo = datos.get("numero_equipo", "")
            numero_jaula = datos.get("numero_jaula", "")
            identificador_repuesto = datos.get("identificador_repuesto", "Name A1")
            texto_referencia = datos.get(
                "texto_referencia",
                f"Equipo {numero_equipo} jaula {numero_jaula} con corte de datos por posible falla en su funcionamiento."
            )
            asunto = f"Ticket centro {centro_nombre} / Falla equipo {numero_equipo} jaula {numero_jaula}".strip()
            ctx.update({
                "numero_equipo": numero_equipo,
                "numero_jaula": numero_jaula,
                "identificador_repuesto": identificador_repuesto,
                "texto_referencia": texto_referencia,
            })
            template_name = "emails/ticket_falla_equipo.html"

        elif tipo_ticket == "falla_sensor":
            tipo_sensor = datos.get("tipo_sensor", "oxígeno")
            profundidad = datos.get("profundidad", "10")
            numero_jaula = datos.get("numero_jaula", "105")
            asunto = f"Ticket - {centro_nombre} - Falla sensor {tipo_sensor} - Prof. {profundidad} mts – Jaula {numero_jaula}"
            ctx.update({
                "tipo_sensor": tipo_sensor,
                "profundidad": profundidad,
                "numero_jaula": numero_jaula,
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
        asunto, html_content = cls.generar_html_ticket(tipo_ticket, datos, personal)
        text_content = strip_tags(html_content)

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

        msg = EmailMultiAlternatives(
            subject=asunto,
            body=text_content,
            from_email=correo_remitente,
            to=to_list,
            cc=cc_list,
            reply_to=[correo_remitente, "soporte@innovex.cl"],
        )

        # Procesar imágenes base64 embebidas para convertirlas en MIME CIDs
        html_final = html_content
        data_uri_pattern = re.compile(r'src=["\']data:image/(png|jpeg|jpg|webp);base64,([A-Za-z0-9+/=]+)["\']', re.IGNORECASE)

        def _sub_img_cid(match):
            img_type = match.group(1).lower()
            if img_type == "jpg":
                img_type = "jpeg"
            b64_data = match.group(2)
            try:
                img_bytes = base64.b64decode(b64_data)
                cid = f"img_{uuid.uuid4().hex[:10]}"
                mime_img = MIMEImage(img_bytes, _subtype=img_type)
                mime_img.add_header("Content-ID", f"<{cid}>")
                mime_img.add_header("Content-Disposition", "inline", filename=f"{cid}.{img_type}")
                msg.attach(mime_img)
                return f'src="cid:{cid}"'
            except Exception:
                return match.group(0)

        html_final = data_uri_pattern.sub(_sub_img_cid, html_final)
        msg.attach_alternative(html_final, "text/html")

        # Adjuntar Guía PDF oficial si se solicita
        if adjuntar_guia:
            guias_dir = getattr(settings, "STORAGE_DIR", Path("storage")) / "guias"
            guia_path = guias_dir / "guia_mantenimiento_correctivo_innovex.pdf"
            if guia_path.exists() and guia_path.is_file():
                msg.attach(
                    filename="Guia_Mantencion_Correctiva_Innovex.pdf",
                    content=guia_path.read_bytes(),
                    mimetype="application/pdf"
                )

        # Enviar correo
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

