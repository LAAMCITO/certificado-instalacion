"""
URL patterns for Portal app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Bitácora (GET + POST on same path)
    path("bitacora", views.bitacora, name="portal_bitacora"),

    # Asistentes
    path("asistentes", views.asistentes, name="portal_asistentes"),

    # Empresas
    path("empresas", views.empresas_get, name="portal_empresas"),

    # Destinatarios (GET + POST on same path)
    path("destinatarios", views.destinatarios, name="portal_destinatarios"),

    # Fechas fin de semana
    path("fechas_fin_semana", views.fechas_fin_semana, name="portal_fechas"),

    # Encargados, Zonas y Técnicos
    path("personal/estructura", views.estructura_personal, name="portal_estructura_personal"),

    # Wiki
    path("wiki/buscar", views.wiki_buscar, name="portal_wiki_buscar"),
    path("wiki/indice", views.wiki_indice, name="portal_wiki_indice"),

    # Música
    path("music/status", views.music_status, name="portal_music_status"),
    path("music/control", views.music_control, name="portal_music_control"),

    # Correos masivos
    path("enviar_correos_masivos", views.enviar_correos_masivos, name="portal_correos"),

    # Tickets de Falla
    path("tickets/centros", views.tickets_centros, name="portal_tickets_centros"),
    path("tickets/previsualizar", views.tickets_previsualizar, name="portal_tickets_previsualizar"),
    path("tickets/enviar", views.tickets_enviar, name="portal_tickets_enviar"),
    path("tickets/historial", views.tickets_historial, name="portal_tickets_historial"),
]
