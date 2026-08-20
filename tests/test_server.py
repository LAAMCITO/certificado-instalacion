"""
Tests para endpoints de la API en Django.
"""

import os
import json
import unittest
from pathlib import Path

# Setup Django test environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from django.test import Client, TestCase
from apps.revisor.services import limpiar_salida_telnet


class TestDjangoAPIServer(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_index(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode("utf-8")
        self.assertIn("Portal de Soporte", content)

    def test_api_autofill(self):
        payload = {
            "texto": "Static hostname: ce-tranqui1\nHardware Model: Lenovo V14 G3 IAP\ninet 10.9.18.37  netmask 255.255.255.255",
            "certificado": {}
        }
        resp = self.client.post(
            "/api/autofill",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        res = resp.json()
        self.assertEqual(res["status"], "ok")
        cert = res["certificado"]
        self.assertEqual(cert["datos_generales"]["location"], "ce-tranqui1")
        self.assertEqual(cert["infraestructura"]["modelo"], "Lenovo V14 G3 IAP")

    def test_api_generate_pdf(self):
        payload = {
            "certificado": {
                "datos_generales": {
                    "location": "ce-tranqui1",
                    "nombre_centro": "CE-TRANQUI1",
                    "numero_ficha": "9999"
                },
                "infraestructura": {},
                "acceso_remoto": {},
                "estacion_camara": {},
                "monitoreo_abiotico": {},
                "ubicaciones": [],
                "equipos_repuesto": [],
                "observaciones": ""
            }
        }
        resp = self.client.post(
            "/api/generate_pdf",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        res = resp.json()
        self.assertEqual(res["status"], "ok")
        self.assertIn("pdf_preview_url", res)

    def test_api_ingreso_tecnico(self):
        payload = {
            "dns": "ce-yelcho.acuimatic.com",
            "clave_pc": "clave-de-prueba",
            "acceso_remoto": "",
            "observaciones": "Name 5 desasociado, llevar pilas o caja de repuesto.\nReponer stock de repuesto, sensor y caja jennic"
        }
        resp = self.client.post(
            "/api/revisor/ingreso_tecnico",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        res = resp.json()
        self.assertEqual(res["status"], "ok")
        resultado = res["resultado"]
        self.assertEqual(resultado["dns"], "ce-yelcho.acuimatic.com")
        self.assertEqual(resultado["clave_pc"], "clave-de-prueba")
        self.assertIn("DNS:ce-yelcho.acuimatic.com", resultado["plantilla_texto"])
        self.assertIn("Clave PC:clave-de-prueba", resultado["plantilla_texto"])
        self.assertIn("Antena status:", resultado["plantilla_texto"])
        self.assertIn("Equipos conectados:", resultado["plantilla_texto"])
        self.assertIn("Voltaje pilas:", resultado["plantilla_texto"])
        self.assertIn("Observaciones:", resultado["plantilla_texto"])
        self.assertIn("Observaciones generales:", resultado["plantilla_texto"])
        self.assertNotIn("Bienvenido al servidor de Telnet!", resultado["plantilla_texto"])
        self.assertIn("documento_live_html", resultado)
        self.assertIn("INFORMACIÓN PARA INGRESO DE TÉCNICO", resultado["documento_live_html"])

    def test_limpiar_salida_telnet(self):
        raw = "Bienvenido al servidor de Telnet!\nEscape character is '^]'\nPancoordinator status\nVersion v2.0.2"
        clean = limpiar_salida_telnet(raw)
        self.assertNotIn("Bienvenido al servidor de Telnet!", clean)
        self.assertNotIn("Escape character", clean)
        self.assertIn("Pancoordinator status", clean)
        self.assertIn("Version v2.0.2", clean)


if __name__ == "__main__":
    unittest.main()
