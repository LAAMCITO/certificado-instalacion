"""
Django models for Certificados app.
"""

import uuid
from django.db import models


class CertificadoInstalacion(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    location = models.CharField(max_length=100, db_index=True)
    nombre_centro = models.CharField(max_length=200, blank=True, default="")
    empresa = models.CharField(max_length=150, blank=True, default="")
    año = models.IntegerField(db_index=True)
    fecha_instalacion = models.CharField(max_length=50, blank=True, default="")
    tecnico_visita = models.CharField(max_length=150, blank=True, default="")
    numero_ficha = models.CharField(max_length=100, blank=True, default="")
    data = models.JSONField(default=dict)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Certificado de Instalación"
        verbose_name_plural = "Certificados de Instalación"
        ordering = ["-año", "-fecha_modificacion", "location"]
        unique_together = [("location", "año")]

    def __str__(self):
        return f"{self.location} ({self.nombre_centro or 'Sin nombre'}) - {self.año}"

    def to_dict(self):
        return self.data if self.data else {
            "datos_generales": {
                "location": self.location,
                "nombre_centro": self.nombre_centro,
                "empresa": self.empresa,
                "fecha_instalacion": self.fecha_instalacion,
                "tecnico_visita": self.tecnico_visita,
                "numero_ficha": self.numero_ficha,
            }
        }
