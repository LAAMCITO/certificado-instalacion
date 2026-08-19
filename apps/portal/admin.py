"""
Django Admin configuration for Portal app.
"""

from django.contrib import admin
from .models import Asistente, Destinatario, Bitacora


@admin.register(Asistente)
class AsistenteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "cargo", "telefono", "correo", "activo", "orden")
    list_editable = ("activo", "orden")
    search_fields = ("nombre", "correo", "telefono")
    list_filter = ("activo", "cargo")


@admin.register(Destinatario)
class DestinatarioAdmin(admin.ModelAdmin):
    list_display = ("id", "empresa", "correo", "activo")
    list_editable = ("activo",)
    search_fields = ("empresa", "correo")
    list_filter = ("activo", "empresa")


@admin.register(Bitacora)
class BitacoraAdmin(admin.ModelAdmin):
    list_display = ("id", "actualizado_en")
    readonly_fields = ("actualizado_en",)
