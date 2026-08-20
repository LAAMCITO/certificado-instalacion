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


class CentroContactoTicket(models.Model):
    empresa = models.CharField(max_length=150, help_text="Empresa o cliente (ej: Cermaq, Mowi, AquaChile)")
    nombre_centro = models.CharField(max_length=150, help_text="Nombre del centro de cultivo")
    codigo_location = models.CharField(max_length=100, blank=True, default="", help_text="Código o location (ej: ch-chidhuapi1, ce-pollollo)")
    zona_geografica = models.ForeignKey(
        ZonaGeografica,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="centros_contacto",
        help_text="Zona geográfica a la que pertenece el centro"
    )
    destinatarios_to = models.TextField(
        blank=True,
        default="",
        help_text="Correos principales (Para / TO) separados por coma, punto y coma o saltos de línea"
    )
    destinatarios_cc = models.TextField(
        blank=True,
        default="",
        help_text="Correos en copia (CC) separados por coma, punto y coma o saltos de línea"
    )
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Centro de Cultivo & Contactos para Tickets"
        verbose_name_plural = "Centros de Cultivo & Contactos para Tickets"
        ordering = ["empresa", "nombre_centro"]

    def __str__(self):
        return f"{self.empresa} - {self.nombre_centro}"

    def to_dict(self):
        return {
            "id": self.id,
            "empresa": self.empresa,
            "nombre_centro": self.nombre_centro,
            "codigo_location": self.codigo_location,
            "zona": self.zona_geografica.nombre if self.zona_geografica else "",
            "zona_id": self.zona_geografica.id if self.zona_geografica else None,
            "destinatarios_to": self.destinatarios_to,
            "destinatarios_cc": self.destinatarios_cc,
            "activo": self.activo,
        }


class HistorialTicketEnviado(models.Model):
    TIPO_CHOICES = [
        ("conexion", "Ticket de Conexión"),
        ("falla_equipo", "Ticket de Falla de Equipo"),
        ("falla_sensor", "Ticket de Falla de Sensor"),
    ]

    tipo_ticket = models.CharField(max_length=50, choices=TIPO_CHOICES)
    empresa = models.CharField(max_length=150)
    centro = models.CharField(max_length=150)
    asunto = models.CharField(max_length=255)
    asistente_nombre = models.CharField(max_length=150)
    destinatarios_to = models.TextField()
    destinatarios_cc = models.TextField(blank=True, default="")
    es_prueba = models.BooleanField(default=False)
    manual_adjunto = models.BooleanField(default=True)
    datos_ticket = models.JSONField(default=dict, blank=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Ticket Enviado"
        verbose_name_plural = "Historial de Tickets Enviados"
        ordering = ["-fecha_envio"]

    def __str__(self):
        modo = " [MODO PRUEBA]" if self.es_prueba else ""
        return f"[{self.get_tipo_ticket_display()}] {self.centro} - {self.asistente_nombre}{modo} ({self.fecha_envio.strftime('%d/%m/%Y %H:%M')})"

