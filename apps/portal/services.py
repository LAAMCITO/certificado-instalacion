"""
Service centralizado para el Portal de Soporte Innovex (Django ORM + SQLite).
"""

import datetime
from .models import Asistente, Destinatario, Bitacora

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

    @classmethod
    def generar_html_correo_fin_semana(cls, personal: dict, fecha_sabado: str, fecha_domingo: str) -> str:
        nombre = personal.get("nombre", "Asistente de Soporte")
        cargo = personal.get("cargo", "ASISTENTE DE SOPORTE")
        telefono = personal.get("telefono", "+56 9 8419 4843")
        correo = personal.get("correo", "soporte@innovex.cl")

        return f"""<!DOCTYPE html>
<html lang="es-cl">
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            color: #333333;
            line-height: 1.5;
            background-color: #f8fafc;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 700px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 8px;
            padding: 30px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }}
        .header-bar {{
            border-bottom: 3px solid #f1c40f;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }}
        .header-title {{
            color: #0f172a;
            font-size: 20px;
            font-weight: bold;
            margin: 0;
        }}
        .signature {{
            margin-top: 35px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
        }}
        .highlight {{
            color: #0284c7;
            font-weight: 600;
        }}
        .notice-box {{
            background: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 12px 16px;
            margin: 20px 0;
            border-radius: 4px;
            color: #92400e;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-bar">
            <div class="header-title">COMUNICADO DE SOPORTE — TURNO FIN DE SEMANA</div>
        </div>

        <p>Estimados (as):</p>
        
        <p>Junto con saludar, informamos que para cualquier requerimiento o solicitud de validación de datos o asistencia técnica remota, se encontrará disponible el siguiente personal de turno este <strong>sábado {fecha_sabado}</strong> y <strong>domingo {fecha_domingo}</strong>:</p>
        
        <div style="background: #f1f5f9; padding: 15px 20px; border-radius: 6px; margin: 20px 0;">
            <p style="margin: 4px 0;"><strong>Asistente de Soporte:</strong> <span class="highlight">{nombre}</span></p>
            <p style="margin: 4px 0;"><strong>Contacto telefónico:</strong> <span class="highlight">{telefono}</span></p>
            <p style="margin: 4px 0;"><strong>Correo electrónico:</strong> <a href="mailto:{correo}" style="color: #0284c7; text-decoration: none;">{correo}</a></p>
        </div>

        <div class="notice-box">
            <strong>Favor de ser posible a los centros:</strong> Indicar disponibilidad de stock de repuestos y uso de los mismos para el apoyo y/o gestión correspondiente.
        </div>

        <p>Para coordinaciones de ingresos técnicos, favor dirigir solicitudes al correo: <a href="mailto:jefe.area@innovex.cl" style="color: #0284c7; font-weight: 600;">jefe.area@innovex.cl</a>.</p>

        <p>Quedamos atentos a sus comentarios y requerimientos.</p>

        <div class="signature">
            <table style="border-collapse: collapse; width: 100%;">
                <tr>
                    <td style="padding-right: 20px; border-right: 2px solid #f1c40f; width: 140px; text-align: center; vertical-align: middle;">
                        <span style="font-size: 26px; font-weight: 900; color: #f1c40f; letter-spacing: -0.5px;">in<span style="color: #0f172a;">novex</span><sup style="font-size: 11px; color: #64748b;">&reg;</sup></span><br>
                        <span style="font-size: 9px; color: #64748b; letter-spacing: 1.5px; font-weight: 600;">SOLUCIONES TECNOLÓGICAS</span>
                    </td>
                    <td style="padding-left: 20px; vertical-align: middle;">
                        <strong style="color: #0f172a; font-size: 15px; text-transform: uppercase;">{nombre}</strong><br>
                        <span style="font-size: 12px; color: #64748b; text-transform: uppercase; font-weight: 600;">{cargo}</span><br>
                        <span style="font-size: 12px; color: #334155;">📞 {telefono}</span> &nbsp;|&nbsp; 
                        <a href="mailto:{correo}" style="font-size: 12px; color: #0284c7; text-decoration: none;">{correo}</a>
                    </td>
                </tr>
            </table>
        </div>
    </div>
</body>
</html>"""

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
