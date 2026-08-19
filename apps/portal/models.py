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


class EncargadoArea(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    telefono = models.CharField(max_length=50, blank=True, default="")
    correo = models.EmailField(blank=True, default="")
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Encargado de Área"
        verbose_name_plural = "Encargados de Área"
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "correo": self.correo,
            "activo": self.activo,
            "zonas": [z.nombre for z in self.zonas.filter(activo=True).order_by("orden", "nombre")],
            "tecnicos": [t.nombre for t in self.tecnicos.filter(activo=True).order_by("orden", "nombre")],
        }


class ZonaGeografica(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    encargado_principal = models.ForeignKey(
        EncargadoArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="zonas",
        help_text="Encargado de área asignado por defecto para esta zona geográfica"
    )
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Zona Geográfica / Área"
        verbose_name_plural = "Zonas Geográficas / Áreas"
        ordering = ["orden", "nombre"]

    def __str__(self):
        enc_name = self.encargado_principal.nombre if self.encargado_principal else "Sin asignar"
        return f"{self.nombre} ({enc_name})"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "encargado": self.encargado_principal.nombre if self.encargado_principal else None,
            "activo": self.activo,
        }


class Tecnico(models.Model):
    nombre = models.CharField(max_length=150)
    encargado_principal = models.ForeignKey(
        EncargadoArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tecnicos",
        help_text="Encargado de área al que reporta habitualmente este técnico"
    )
    telefono = models.CharField(max_length=50, blank=True, default="")
    correo = models.EmailField(blank=True, default="")
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Técnico de Terreno"
        verbose_name_plural = "Técnicos de Terreno"
        ordering = ["orden", "nombre"]

    def __str__(self):
        enc_name = self.encargado_principal.nombre if self.encargado_principal else "Sin asignar"
        return f"{self.nombre} ({enc_name})"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "encargado": self.encargado_principal.nombre if self.encargado_principal else None,
            "telefono": self.telefono,
            "correo": self.correo,
            "activo": self.activo,
        }
