"""
Django Admin configuration for Certificados app.
"""

from django.contrib import admin
from .models import CertificadoInstalacion


@admin.register(CertificadoInstalacion)
class CertificadoInstalacionAdmin(admin.ModelAdmin):
    list_display = ("location", "nombre_centro", "empresa", "año", "fecha_instalacion", "tecnico_visita", "fecha_modificacion")
    search_fields = ("location", "nombre_centro", "empresa", "tecnico_visita", "numero_ficha")
    list_filter = ("año", "empresa")
    readonly_fields = ("uuid", "fecha_creacion", "fecha_modificacion")
