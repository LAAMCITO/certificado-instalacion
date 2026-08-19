"""
Django Admin configuration for Portal app.
"""

from django.contrib import admin
from .models import Asistente, Destinatario, Bitacora, EncargadoArea, ZonaGeografica, Tecnico


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


class ZonaInline(admin.TabularInline):
    model = ZonaGeografica
    extra = 1
    fields = ("nombre", "orden", "activo")


class TecnicoInline(admin.TabularInline):
    model = Tecnico
    extra = 1
    fields = ("nombre", "telefono", "correo", "orden", "activo")


@admin.register(EncargadoArea)
class EncargadoAreaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "telefono", "correo", "activo", "orden", "total_zonas", "total_tecnicos")
    list_editable = ("activo", "orden")
    search_fields = ("nombre", "correo", "telefono")
    list_filter = ("activo",)
    inlines = [ZonaInline, TecnicoInline]

    def total_zonas(self, obj):
        return obj.zonas.count()
    total_zonas.short_description = "Zonas Asignadas"

    def total_tecnicos(self, obj):
        return obj.tecnicos.count()
    total_tecnicos.short_description = "Técnicos a Cargo"


@admin.register(ZonaGeografica)
class ZonaGeograficaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "encargado_principal", "activo", "orden")
    list_editable = ("encargado_principal", "activo", "orden")
    search_fields = ("nombre", "encargado_principal__nombre")
    list_filter = ("activo", "encargado_principal")


@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "encargado_principal", "telefono", "correo", "activo", "orden")
    list_editable = ("encargado_principal", "activo", "orden")
    search_fields = ("nombre", "encargado_principal__nombre", "telefono", "correo")
    list_filter = ("activo", "encargado_principal")
