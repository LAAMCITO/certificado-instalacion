"""
Views for Portal app – Dashboard, bitácora, destinatarios, correos, wiki, música.
"""

import json
import subprocess
import threading

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .services import PortalService


def _parse_json_body(request):
    """Parse JSON body from request."""
    try:
        return json.loads(request.body.decode("utf-8"))
    except Exception:
        return {}


# ──────────────────────────────────────────────
# GET endpoints
# ──────────────────────────────────────────────

@require_GET
def bitacora_get(request):
    """GET /api/bitacora"""
    bitacora = PortalService.obtener_bitacora()
    return JsonResponse({"status": "ok", **bitacora})


@require_GET
def asistentes(request):
    """GET /api/asistentes"""
    asistentes_data = PortalService.obtener_asistentes()
    return JsonResponse({"status": "ok", "asistentes": asistentes_data})


@require_GET
def destinatarios_get(request):
    """GET /api/destinatarios"""
    destinatarios_data = PortalService.obtener_destinatarios()
    return JsonResponse({"status": "ok", "destinatarios": destinatarios_data})


@require_GET
def fechas_fin_semana(request):
    """GET /api/fechas_fin_semana"""
    sab, dom, sem = PortalService.calcular_fechas_fin_semana_actual()
    return JsonResponse({
        "status": "ok",
        "fecha_sabado": sab,
        "fecha_domingo": dom,
        "semana": sem,
    })


@require_GET
def estructura_personal(request):
    """GET /api/personal/estructura"""
    data = PortalService.obtener_estructura_personal()
    return JsonResponse(data)


@require_GET
def wiki_buscar(request):
    """GET /api/wiki/buscar?q=..."""
    q = request.GET.get("q", "")
    res = PortalService.buscar_trac_wiki(q)
    return JsonResponse({"status": "ok", **res})


@require_GET
def wiki_indice(request):
    """GET /api/wiki/indice"""
    res = PortalService.obtener_indice_trac_wiki()
    return JsonResponse({"status": "ok", **res})


@require_GET
def music_status(request):
    """GET /api/music/status"""
    status_data = {
        "status": "stopped",
        "title": "Portal de Soporte Innovex",
        "artist": "Música Host",
    }
    try:
        res_st = subprocess.run(
            ["playerctl", "status"], capture_output=True, text=True, timeout=2
        )
        if res_st.returncode == 0:
            status_data["status"] = res_st.stdout.strip().lower()
            t_st = subprocess.run(
                ["playerctl", "metadata", "title"],
                capture_output=True, text=True, timeout=2,
            )
            if t_st.returncode == 0 and t_st.stdout.strip():
                status_data["title"] = t_st.stdout.strip()
            a_st = subprocess.run(
                ["playerctl", "metadata", "artist"],
                capture_output=True, text=True, timeout=2,
            )
            if a_st.returncode == 0 and a_st.stdout.strip():
                status_data["artist"] = a_st.stdout.strip()
    except Exception:
        pass
    return JsonResponse(status_data)


@require_GET
def music_control(request):
    """GET /api/music/control?action=...&query=..."""
    action = request.GET.get("action", "")
    commands = {
        "volup": ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"],
        "voldn": ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"],
        "mute": ["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"],
        "play": ["playerctl", "play-pause"],
        "next": ["playerctl", "next"],
        "prev": ["playerctl", "previous"],
    }
    if action in commands:
        try:
            subprocess.run(commands[action], timeout=3)
            return JsonResponse({"status": "ok"})
        except Exception as exc:
            return JsonResponse({"status": "error", "message": str(exc)})
    return JsonResponse({"status": "ok"})


# ──────────────────────────────────────────────
# POST endpoints
# ──────────────────────────────────────────────

@csrf_exempt
def bitacora(request):
    """GET/POST /api/bitacora – dispatch based on method."""
    if request.method == "GET":
        return bitacora_get(request)
    elif request.method == "POST":
        body = _parse_json_body(request)
        texto = body.get("texto", "")
        res = PortalService.actualizar_bitacora(texto)
        return JsonResponse(res)
    return JsonResponse({"status": "error", "mensaje": "Método no permitido"}, status=405)


@csrf_exempt
def destinatarios(request):
    """GET/POST /api/destinatarios – dispatch based on method."""
    if request.method == "GET":
        return destinatarios_get(request)
    elif request.method == "POST":
        body = _parse_json_body(request)
        action = body.get("action", "")

        if action == "toggle_destinatario":
            dest_id = int(body.get("id", 0))
            activo = bool(body.get("activo", True))
            res = PortalService.toggle_destinatario(dest_id, activo)
            return JsonResponse(res)
        elif action == "create":
            empresa = body.get("empresa", "")
            correo = body.get("correo", "")
            res = PortalService.crear_destinatario(empresa, correo)
            return JsonResponse(res)
        elif action == "delete_destinatario":
            dest_id = int(body.get("id", 0))
            res = PortalService.eliminar_destinatario(dest_id)
            return JsonResponse(res)
        else:
            return JsonResponse(
                {"status": "error", "mensaje": "Acción desconocida"}, status=400
            )
    return JsonResponse({"status": "error", "mensaje": "Método no permitido"}, status=405)


@csrf_exempt
@require_POST
def enviar_correos_masivos(request):
    """POST /api/enviar_correos_masivos – Despacho asíncrono en segundo plano"""
    body = _parse_json_body(request)
    semana = body.get("semana")
    personal_id = body.get("personal_id")
    fecha_sabado = body.get("fecha_sabado") or ""
    fecha_domingo = body.get("fecha_domingo") or ""
    correo_prueba = body.get("correo_prueba", "").strip()

    def _tarea_envio_asincrono():
        try:
            PortalService.enviar_correos_masivos(
                semana=semana,
                personal_id=personal_id,
                fecha_sabado=fecha_sabado,
                fecha_domingo=fecha_domingo,
                correo_prueba=correo_prueba,
            )
        except Exception as exc:
            print(f"❌ Error en hilo de envío de correos masivos: {exc}")

    hilo = threading.Thread(target=_tarea_envio_asincrono)
    hilo.daemon = True
    hilo.start()

    mensaje = (
        f"Se inició el despacho en MODO PRUEBA a {correo_prueba} en segundo plano."
        if correo_prueba
        else "🚀 Se inició el envío de correos masivos en segundo plano. Se despacharán a todas las empresas en breve."
    )

    return JsonResponse({
        "status": "ok",
        "mensaje": mensaje,
        "emails_enviados": 1,
        "modo_prueba": bool(correo_prueba),
    })


# ──────────────────────────────────────────────
# Vistas para Módulo de Tickets de Falla
# ──────────────────────────────────────────────

@csrf_exempt
def tickets_centros(request):
    """GET/POST /api/tickets/centros"""
    if request.method == "GET":
        centros = PortalService.obtener_centros_tickets()
        return JsonResponse({"status": "ok", "centros": centros})

    elif request.method == "POST":
        body = _parse_json_body(request)
        action = body.get("action", "save")
        if action == "delete":
            cid = body.get("id")
            res = PortalService.eliminar_centro_ticket(cid)
            return JsonResponse(res)
        else:
            try:
                res = PortalService.guardar_centro_ticket(body)
                return JsonResponse(res)
            except ValueError as ve:
                return JsonResponse({"status": "error", "mensaje": str(ve)}, status=400)
            except Exception as exc:
                return JsonResponse({"status": "error", "mensaje": str(exc)}, status=500)

    return JsonResponse({"status": "error", "mensaje": "Método no permitido"}, status=405)


@csrf_exempt
@require_POST
def tickets_previsualizar(request):
    """POST /api/tickets/previsualizar"""
    body = _parse_json_body(request)
    tipo_ticket = body.get("tipo_ticket", "conexion")
    datos = body.get("datos", {})

    try:
        personal = PortalService._obtener_datos_personal(datos.get("personal_id"))
        asunto, html = PortalService.generar_html_ticket(tipo_ticket, datos, personal)
        return JsonResponse({
            "status": "ok",
            "asunto": asunto,
            "html": html,
            "personal": personal,
        })
    except Exception as exc:
        return JsonResponse({"status": "error", "mensaje": str(exc)}, status=400)


@csrf_exempt
@require_POST
def tickets_enviar(request):
    """POST /api/tickets/enviar"""
    body = _parse_json_body(request)
    tipo_ticket = body.get("tipo_ticket", "conexion")
    datos = body.get("datos", {})
    personal_id = body.get("personal_id") or datos.get("personal_id")
    destinatarios_to = body.get("destinatarios_to", "")
    destinatarios_cc = body.get("destinatarios_cc", "")
    correo_prueba = body.get("correo_prueba", "").strip()
    adjuntar_guia = body.get("adjuntar_guia", True)

    try:
        res = PortalService.enviar_correo_ticket(
            tipo_ticket=tipo_ticket,
            datos=datos,
            personal_id=personal_id,
            destinatarios_to=destinatarios_to,
            destinatarios_cc=destinatarios_cc,
            correo_prueba=correo_prueba,
            adjuntar_guia=adjuntar_guia,
        )
        return JsonResponse(res)
    except Exception as exc:
        return JsonResponse({"status": "error", "mensaje": str(exc)}, status=400)


@require_GET
def tickets_historial(request):
    """GET /api/tickets/historial"""
    historial = PortalService.obtener_historial_tickets()
    return JsonResponse({"status": "ok", "historial": historial})


