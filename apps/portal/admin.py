"""
Django Admin configuration for Portal app.
"""

from django.contrib import admin
from .models import (
    Empresa, Asistente, Destinatario, Bitacora, EncargadoArea,
    ZonaGeografica, Tecnico, CentroContactoTicket, HistorialTicketEnviado
)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "codigo", "activo", "total_centros", "total_destinatarios")
    list_editable = ("activo",)
    search_fields = ("nombre", "codigo")
    list_filter = ("activo",)

    def total_centros(self, obj):
        return obj.centros_ticket.count()
    total_centros.short_description = "Centros Registrados"

    def total_destinatarios(self, obj):
        return obj.destinatarios.count()
    total_destinatarios.short_description = "Destinatarios Masivos"


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


@admin.register(CentroContactoTicket)
class CentroContactoTicketAdmin(admin.ModelAdmin):
    list_display = ("id", "empresa", "nombre_centro", "codigo_location", "zona_geografica", "activo")
    list_editable = ("activo",)
    search_fields = ("empresa", "nombre_centro", "codigo_location", "destinatarios_to", "destinatarios_cc")
    list_filter = ("activo", "empresa", "zona_geografica")


@admin.register(HistorialTicketEnviado)
class HistorialTicketEnviadoAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo_ticket", "empresa", "centro", "asistente_nombre", "es_prueba", "fecha_envio")
    search_fields = ("empresa", "centro", "asunto", "asistente_nombre", "destinatarios_to")
    list_filter = ("tipo_ticket", "es_prueba", "empresa", "fecha_envio")
    readonly_fields = ("fecha_envio",)

