"""
Django models for Portal app.
"""

from django.db import models


class Asistente(models.Model):
    nombre = models.CharField(max_length=150)
    cargo = models.CharField(max_length=150, default="ASISTENTE DE SOPORTE")
    telefono = models.CharField(max_length=50, blank=True)
    correo = models.EmailField()
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asistente de Soporte"
        verbose_name_plural = "Asistentes de Soporte"
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cargo": self.cargo,
            "telefono": self.telefono,
            "correo": self.correo,
            "activo": self.activo,
        }


class Destinatario(models.Model):
    empresa = models.CharField(max_length=150)
    correo = models.EmailField()
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Destinatario de Correo"
        verbose_name_plural = "Destinatarios de Correos"
        ordering = ["empresa", "correo"]

    def __str__(self):
        return f"{self.empresa} - {self.correo} ({'Activo' if self.activo else 'Inactivo'})"

    def to_dict(self):
        return {
            "id": self.id,
            "empresa": self.empresa,
            "correo": self.correo,
            "activo": self.activo,
        }


class Bitacora(models.Model):
    texto = models.TextField(blank=True, default="")
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bitácora / Pizarra"
        verbose_name_plural = "Bitácora / Pizarra"

    def __str__(self):
        return f"Bitácora ({self.actualizado_en.strftime('%d/%m/%Y %H:%M') if self.actualizado_en else 'Sin fecha'})"

    def to_dict(self):
        return {
            "texto": self.texto,
            "actualizado_en": self.actualizado_en.strftime("%d/%m/%Y %H:%M") if self.actualizado_en else "",
        }
