"""
Pruebas unitarias para el módulo de Tickets de Falla (Conexión, Equipo y Sensor).
"""

import os
import base64
import django
from django.test import TestCase, Client
from django.core import mail

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.portal.models import CentroContactoTicket, HistorialTicketEnviado, Asistente
from apps.portal.services import PortalService


class TicketsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.asistente = Asistente.objects.create(
            nombre="Leonardo Araneda",
            cargo="ASISTENTE DE SOPORTE",
            telefono="+56 9 8419 4913",
            correo="leonardo.araneda@innovex.cl",
            orden=1
        )
        self.centro = CentroContactoTicket.objects.create(
            empresa="CERMAQ",
            nombre_centro="Chidhuapi 1",
            codigo_location="ch-chidhuapi1",
            destinatarios_to="jefe.chidhuapi@cermaq.com",
            destinatarios_cc="soporte.cermaq@innovex.cl",
            activo=True
        )

    def test_generar_html_ticket_conexion(self):
        datos = {
            "empresa": "CERMAQ",
            "nombre_centro": "Chidhuapi 1",
            "personal_id": self.asistente.id,
            "imagen_evidencia": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
        }
        asunto, html = PortalService.generar_html_ticket("conexion", datos)
        self.assertIn("Ticket - Chidhuapi 1 / CONEXIÓN.", asunto)
        self.assertIn("Actualmente no es posible visualizar", html)
        self.assertIn("Leonardo Araneda", html)
        self.assertIn("Asistente de Soporte Intermedio", html)
        self.assertIn("data:image/png;base64,", html)

    def test_generar_html_ticket_falla_equipo(self):
        datos = {
            "empresa": "CERMAQ",
            "nombre_centro": "Chidhuapi 1",
            "numero_equipo": "10",
            "numero_jaula": "204",
            "ubicacion": "Pontón",
            "identificador_repuesto": "Name A1",
            "personal_id": self.asistente.id,
        }
        asunto, html = PortalService.generar_html_ticket("falla_equipo", datos)
        self.assertIn("Ticket - Chidhuapi 1 - Falla de equipo 10", asunto)
        self.assertIn("Pontón", html)
        self.assertIn("Importante:", html)
        self.assertIn("Mantención correctiva Jennic", html)

    def test_generar_html_ticket_falla_sensor(self):
        datos = {
            "empresa": "AQUACHILE",
            "nombre_centro": "Sa-Lleuna",
            "tipo_sensor": "oxígeno",
            "profundidad": "10",
            "numero_jaula": "105",
            "personal_id": self.asistente.id,
        }
        asunto, html = PortalService.generar_html_ticket("falla_sensor", datos)
        self.assertIn("Ticket - Sa-Lleuna - Falla sensor oxígeno - Prof. 10 mts – Jaula 105", asunto)
        self.assertIn("Retirar la tapa amarilla", html)
        self.assertIn("Mantención correctiva del sensor", html)

    def test_enviar_ticket_conexion_sin_guia_mime_related(self):
        mail.outbox = []
        b64_dummy = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        datos = {
            "empresa": "CERMAQ",
            "nombre_centro": "Chidhuapi 1",
            "personal_id": self.asistente.id,
            "imagen_evidencia": b64_dummy,
        }
        res = PortalService.enviar_correo_ticket(
            tipo_ticket="conexion",
            datos=datos,
            personal_id=self.asistente.id,
            destinatarios_to="cliente@empresa.com",
            correo_prueba="prueba@innovex.cl",
            adjuntar_guia=True  # Debe forzarse a False internamente por ser conexion
        )
        self.assertEqual(res["status"], "ok")
        self.assertTrue(res["es_prueba"])
        self.assertEqual(len(mail.outbox), 1)

        sent = mail.outbox[0]
        self.assertEqual(sent.to, ["prueba@innovex.cl"])

        # Verificar estructura MIME
        mime_msg = sent.message()
        content_types = [p.get_content_type() for p in mime_msg.walk()]
        self.assertIn("multipart/related", content_types)
        self.assertIn("text/html", content_types)
        self.assertIn("image/png", content_types)
        # Asegurarse que NO se adjuntó el PDF en conexión
        self.assertNotIn("application/pdf", content_types)

        # Historial
        h = HistorialTicketEnviado.objects.first()
        self.assertIsNotNone(h)
        self.assertEqual(h.centro, "Chidhuapi 1")
        self.assertFalse(h.manual_adjunto)

    def test_enviar_ticket_equipo_con_pdf_y_imagenes(self):
        mail.outbox = []
        b64_dummy = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        datos = {
            "empresa": "CERMAQ",
            "nombre_centro": "Chidhuapi 1",
            "numero_equipo": "5",
            "numero_jaula": "101",
            "identificador_repuesto": "Name A1",
            "imagen_grafica": b64_dummy,
            "imagen_defectuoso": b64_dummy,
            "imagen_repuesto": b64_dummy,
        }
        res = PortalService.enviar_correo_ticket(
            tipo_ticket="falla_equipo",
            datos=datos,
            personal_id=self.asistente.id,
            destinatarios_to="cliente@empresa.com",
            correo_prueba="tester@innovex.cl",
            adjuntar_guia=True
        )
        self.assertEqual(res["status"], "ok")
        sent = mail.outbox[0]
        mime_msg = sent.message()
        content_types = [p.get_content_type() for p in mime_msg.walk()]
        self.assertIn("multipart/mixed", content_types)
        self.assertIn("multipart/related", content_types)
        self.assertIn("application/pdf", content_types)
        self.assertIn("image/png", content_types)

    def test_api_tickets_endpoints(self):
        # 1. GET Centros
        res_centros = self.client.get("/api/tickets/centros")
        self.assertEqual(res_centros.status_code, 200)
        self.assertIn("centros", res_centros.json())

        # 2. POST Previsualizar
        res_prev = self.client.post(
            "/api/tickets/previsualizar",
            data={
                "tipo_ticket": "falla_sensor",
                "datos": {
                    "empresa": "CAMANCHACA",
                    "nombre_centro": "Pollollo",
                    "tipo_sensor": "oxígeno",
                    "profundidad": "15",
                    "numero_jaula": "102",
                }
            },
            content_type="application/json"
        )
        self.assertEqual(res_prev.status_code, 200)
        json_prev = res_prev.json()
        self.assertEqual(json_prev["status"], "ok")
        self.assertIn("Pollollo", json_prev["asunto"])

        # 3. POST Enviar
        res_send = self.client.post(
            "/api/tickets/enviar",
            data={
                "tipo_ticket": "falla_sensor",
                "datos": {
                    "empresa": "CAMANCHACA",
                    "nombre_centro": "Pollollo",
                },
                "correo_prueba": "tester@innovex.cl",
                "adjuntar_guia": True,
            },
            content_type="application/json"
        )
        self.assertEqual(res_send.status_code, 200)
        self.assertEqual(res_send.json()["status"], "ok")

        # 4. GET Historial
        res_hist = self.client.get("/api/tickets/historial")
        self.assertEqual(res_hist.status_code, 200)
        self.assertGreaterEqual(len(res_hist.json()["historial"]), 1)
