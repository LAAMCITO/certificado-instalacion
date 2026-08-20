"""
URL patterns for Revisor app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("ssh_autofill", views.ssh_autofill, name="revisor_ssh_autofill"),
    path("revisor/verificar", views.verificar_equipo, name="revisor_verificar"),
    path("revisor/generar_plantilla", views.generar_plantilla, name="revisor_generar_plantilla"),
    path("revisor/ingreso_tecnico", views.ingreso_tecnico, name="revisor_ingreso_tecnico"),
    path("revisor/generar_plantilla_ingreso", views.generar_plantilla_ingreso, name="revisor_plantilla_ingreso"),
]
