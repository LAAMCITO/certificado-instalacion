"""
Views for Portal app – Dashboard, bitácora, destinatarios, correos, wiki, música.
"""

import json
import subprocess

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
    """POST /api/enviar_correos_masivos"""
    body = _parse_json_body(request)
    personal_id = body.get("personal_id")
    fecha_sabado = body.get("fecha_sabado") or ""
    fecha_domingo = body.get("fecha_domingo") or ""
    correo_prueba = body.get("correo_prueba", "").strip()

    asistentes_data = PortalService.obtener_asistentes()
    personal = next(
        (p for p in asistentes_data if str(p.get("id")) == str(personal_id)),
        None,
    )
    if not personal and asistentes_data:
        personal = asistentes_data[0]
    elif not personal:
        personal = {
            "nombre": "Asistente de Soporte",
            "cargo": "ASISTENTE DE SOPORTE",
            "telefono": "+56 9 8419 4843",
            "correo": "soporte@innovex.cl",
        }

    html_content = PortalService.generar_html_correo_fin_semana(
        personal, fecha_sabado, fecha_domingo
    )
    destinatarios_data = PortalService.obtener_destinatarios()
    activos = [d for d in destinatarios_data if d.get("activo")]

    return JsonResponse({
        "status": "ok",
        "mensaje": (
            f"Correo generado exitosamente para {len(activos)} destinatarios activos."
            if not correo_prueba
            else f"Modo prueba: correo generado para {correo_prueba}."
        ),
        "html_correo": html_content,
        "destinatarios_count": len(activos),
        "personal": personal,
        "modo_prueba": bool(correo_prueba),
    })
