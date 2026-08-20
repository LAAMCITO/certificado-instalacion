"""
Views for Certificados app – CRUD, autofill, PDF generation, evidencias.
"""

import base64
import json
from datetime import datetime
from pathlib import Path

from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .services import CertificadoService, BASE_STORAGE
from apps.core.utils.autofill import procesar_autofill
from apps.core.pdf.generador_pdf import GeneradorPDF


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
def listar_certificados(request):
    """GET /api/list?año=2026"""
    año_str = request.GET.get("año") or str(datetime.now().year)
    try:
        año = int(año_str)
    except ValueError:
        año = datetime.now().year

    certificados = CertificadoService.listar_certificados(año)
    return JsonResponse({
        "status": "ok",
        "año": año,
        "certificados": certificados,
    })


@require_GET
def pdf_preview(request, año: str, location: str, nombre_pdf: str = ""):
    """GET /api/pdf_preview/<año>/<location>/"""
    nombre_pdf_gen = f"certificado_inst_{location}.pdf"
    dir_location = BASE_STORAGE / str(año) / location

    posibles = [
        dir_location / nombre_pdf_gen,
        dir_location / "certificado.pdf",
    ]
    for p in posibles:
        if p.exists() and p.is_file():
            return FileResponse(
                open(p, "rb"),
                content_type="application/pdf",
                filename=nombre_pdf_gen,
            )
    raise Http404("PDF no encontrado")


# ──────────────────────────────────────────────
# POST endpoints
# ──────────────────────────────────────────────

@csrf_exempt
@require_POST
def procesar_autofill_view(request):
    """POST /api/autofill"""
    body = _parse_json_body(request)
    texto = body.get("texto", "")
    certificado_actual = body.get("certificado", {})
    if body.get("limpiar_previos", False):
        certificado_actual["motes"] = []
        certificado_actual["ubicaciones"] = []
        certificado_actual["equipos_repuesto"] = []
        certificado_actual["configuracion_alarmas"] = []

    try:
        resultado = procesar_autofill(certificado_actual, texto)
        return JsonResponse({
            "status": "ok",
            "certificado": certificado_actual,
            "resumen": resultado.get("resumen", []),
            "exito": resultado.get("exito", False),
        })
    except Exception as exc:
        return JsonResponse({
            "status": "error",
            "mensaje": str(exc),
        })


@csrf_exempt
@require_POST
def guardar_certificado(request):
    """POST /api/save"""
    body = _parse_json_body(request)
    certificado = body.get("certificado", {})
    datos_gen = certificado.get("datos_generales", {})
    location = datos_gen.get("location") or "sin_location"
    año = datetime.now().year

    ruta_json = CertificadoService.guardar_certificado(certificado, location, año)
    CertificadoService.copiar_evidencias_a_certificado(location, año)

    return JsonResponse({
        "status": "ok",
        "mensaje": "Certificado guardado correctamente",
        "ruta": str(ruta_json),
        "location": location,
        "año": año,
    })


@csrf_exempt
@require_POST
def generar_pdf(request):
    """POST /api/generate_pdf"""
    body = _parse_json_body(request)
    certificado = body.get("certificado", {})
    datos_gen = certificado.get("datos_generales", {})
    location = datos_gen.get("location") or "sin_location"
    año = datetime.now().year

    dir_cert = BASE_STORAGE / str(año) / location
    dir_cert.mkdir(parents=True, exist_ok=True)

    ruta_json = CertificadoService.guardar_certificado(certificado, location, año)
    CertificadoService.copiar_evidencias_a_certificado(location, año)

    nombre_pdf = f"certificado_inst_{location}.pdf"
    ruta_pdf = dir_cert / nombre_pdf
    dir_evidencias = dir_cert / "evidencias"

    GeneradorPDF().generar(
        certificado,
        str(ruta_pdf),
        carpeta_evidencias=dir_evidencias if dir_evidencias.exists() else None,
    )

    pdf_preview_url = f"/api/pdf_preview/{año}/{location}/{nombre_pdf}"

    return JsonResponse({
        "status": "ok",
        "mensaje": "PDF generado con éxito",
        "ruta_pdf": str(ruta_pdf),
        "pdf_preview_url": pdf_preview_url,
    })


@csrf_exempt
@require_POST
def cargar_certificado(request):
    """POST /api/load"""
    body = _parse_json_body(request)
    location = body.get("location")
    año = int(body.get("año", datetime.now().year))
    if not location:
        return JsonResponse({"status": "error", "mensaje": "Location es requerido"}, status=400)

    try:
        cert_data = CertificadoService.cargar_certificado(location, año)
        return JsonResponse({"status": "ok", "certificado": cert_data})
    except FileNotFoundError:
        return JsonResponse(
            {"status": "error", "mensaje": f"No se encontró certificado para {location}"},
            status=404,
        )


@csrf_exempt
@require_POST
def eliminar_certificado(request):
    """POST /api/delete"""
    body = _parse_json_body(request)
    location = body.get("location") or body.get("datos_generales", {}).get("location")
    año = int(body.get("año", datetime.now().year))
    if not location:
        return JsonResponse({"status": "error", "mensaje": "Location es requerido"}, status=400)

    exito = CertificadoService.eliminar_certificado(location, año)
    if exito:
        return JsonResponse({
            "status": "ok",
            "mensaje": f"Certificado de {location} eliminado correctamente",
            "location": location,
        })
    return JsonResponse(
        {"status": "error", "mensaje": f"No se encontró el certificado de {location}"},
        status=404,
    )


@csrf_exempt
@require_POST
def upload_evidencia(request):
    """POST /api/upload_evidencia"""
    body = _parse_json_body(request)
    nombre = body.get("nombre", "foto.jpg")
    base64_data = body.get("base64", "")
    location = body.get("location", "sin_location")

    if "," in base64_data:
        base64_data = base64_data.split(",", 1)[1]

    file_bytes = base64.b64decode(base64_data)
    año = datetime.now().year
    dir_ev = Path(f"storage/certificados/{año}") / location / "evidencias"
    dir_ev.mkdir(parents=True, exist_ok=True)

    dest_file = dir_ev / nombre
    dest_file.write_bytes(file_bytes)

    return JsonResponse({
        "status": "ok",
        "mensaje": "Evidencia subida correctamente",
        "ruta": str(dest_file),
        "nombre": nombre,
    })


@csrf_exempt
@require_POST
def upload_alarmas(request):
    """POST /api/upload_alarmas"""
    body = _parse_json_body(request)
    nombre = body.get("nombre", "alarmas.xlsx")
    base64_data = body.get("base64", "")
    location = body.get("location", "sin_location")

    if "," in base64_data:
        base64_data = base64_data.split(",", 1)[1]

    from apps.core.utils.excel_parser import parsear_alarmas_excel

    file_bytes = base64.b64decode(base64_data)
    año = datetime.now().year
    dir_ev = Path(f"storage/certificados/{año}") / location / "evidencias"
    dir_ev.mkdir(parents=True, exist_ok=True)

    dest_file = dir_ev / nombre
    dest_file.write_bytes(file_bytes)

    alarmas = parsear_alarmas_excel(dest_file)
    return JsonResponse({
        "status": "ok",
        "mensaje": "Planilla de alarmas procesada",
        "alarmas": alarmas,
    })


@csrf_exempt
@require_POST
def parse_alarmas_texto(request):
    """POST /api/parse_alarmas_texto"""
    body = _parse_json_body(request)
    texto = body.get("texto", "")

    from apps.core.utils.excel_parser import parsear_alarmas_texto

    alarmas = parsear_alarmas_texto(texto)
    return JsonResponse({
        "status": "ok",
        "mensaje": f"{len(alarmas)} alarmas procesadas",
        "alarmas": alarmas,
    })
