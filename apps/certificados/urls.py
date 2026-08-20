"""
URL patterns for Certificados app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # GET
    path("list", views.listar_certificados, name="cert_list"),
    path("pdf_preview/<str:año>/<str:location>/", views.pdf_preview, name="cert_pdf_preview"),
    path("pdf_preview/<str:año>/<str:location>/<str:nombre_pdf>", views.pdf_preview, name="cert_pdf_preview_named"),

    # POST
    path("autofill", views.procesar_autofill_view, name="cert_autofill"),
    path("save", views.guardar_certificado, name="cert_save"),
    path("generate_pdf", views.generar_pdf, name="cert_generate_pdf"),
    path("load", views.cargar_certificado, name="cert_load"),
    path("delete", views.eliminar_certificado, name="cert_delete"),
    path("upload_evidencia", views.upload_evidencia, name="cert_upload_evidencia"),
    path("upload_alarmas", views.upload_alarmas, name="cert_upload_alarmas"),
    path("parse_alarmas_texto", views.parse_alarmas_texto, name="cert_parse_alarmas"),
]
