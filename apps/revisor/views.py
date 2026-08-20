"""
Views for Revisor app – SSH autofill, equipment verification, templates.
"""

import json
import traceback

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .services import RevisorService
from apps.core.constants.empresas import parse_location_info
from apps.core.utils.autofill import procesar_autofill


def _parse_json_body(request):
    """Parse JSON body from request."""
    try:
        return json.loads(request.body.decode("utf-8"))
    except Exception:
        return {}


@csrf_exempt
@require_POST
def ssh_autofill(request):
    """POST /api/ssh_autofill"""
    body = _parse_json_body(request)
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
            if nom_c and (
                not certificado["datos_generales"].get("nombre_centro")
                or certificado["datos_generales"].get("nombre_centro") == loc_clean.upper()
            ):
                certificado["datos_generales"]["nombre_centro"] = nom_c
            if emp and not certificado["datos_generales"].get("empresa"):
                certificado["datos_generales"]["empresa"] = emp

        return JsonResponse({
            "status": "ok",
            "certificado": certificado,
            "resumen": resumen_dict.get("resumen", []),
            "exito": resumen_dict.get("exito", False),
        })
    except Exception as exc:
        traceback.print_exc()
        return JsonResponse({"status": "error", "mensaje": str(exc)})


@csrf_exempt
@require_POST
def verificar_equipo(request):
    """POST /api/revisor/verificar"""
    body = _parse_json_body(request)
    resultado = RevisorService.verificar_equipo(body)

    if (
        resultado.get("error")
        and not resultado.get("log_cacheton_raw")
        and not resultado.get("status_raw")
        and not resultado.get("motes_raw")
        and not resultado.get("motes_texto_raw")
    ):
        return JsonResponse({
            "status": "error",
            "mensaje": f"Error de conexión: {resultado.get('error')}",
            "resultado": resultado,
        })
    return JsonResponse({"status": "ok", "resultado": resultado})


@csrf_exempt
@require_POST
def generar_plantilla(request):
    """POST /api/revisor/generar_plantilla"""
    body = _parse_json_body(request)
    plantilla = RevisorService.generar_plantilla_texto(body)
    html_doc = RevisorService.generar_documento_live_html(body)
    return JsonResponse({
        "status": "ok",
        "plantilla_texto": plantilla,
        "documento_live_html": html_doc,
    })


@csrf_exempt
@require_POST
def ingreso_tecnico(request):
    """POST /api/revisor/ingreso_tecnico"""
    body = _parse_json_body(request)
    resultado = RevisorService.consultar_ingreso_tecnico_remoto(body)
    return JsonResponse({"status": "ok", "resultado": resultado})


@csrf_exempt
@require_POST
def generar_plantilla_ingreso(request):
    """POST /api/revisor/generar_plantilla_ingreso"""
    body = _parse_json_body(request)
    plantilla = RevisorService.generar_plantilla_ingreso_tecnico(body)
    html_doc = RevisorService.generar_documento_ingreso_tecnico_html(body)
    return JsonResponse({
        "status": "ok",
        "plantilla_texto": plantilla,
        "documento_live_html": html_doc,
    })
