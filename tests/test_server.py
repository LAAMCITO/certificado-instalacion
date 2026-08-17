import unittest
import threading
import urllib.request
import json
import time
from src.server.server import iniciar_servidor_http


class TestCertificadoServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server, cls.puerto = iniciar_servidor_http(puerto=9876)
        cls.base_url = f"http://127.0.0.1:{cls.puerto}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_get_index(self):
        req = urllib.request.Request(f"{self.base_url}/")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            html = resp.read().decode("utf-8")
            self.assertIn("Certificado de Instalación", html)

    def test_api_autofill(self):
        payload = {
            "texto": "Static hostname: ce-tranqui1\nHardware Model: Lenovo V14 G3 IAP\ninet 10.9.18.37  netmask 255.255.255.255",
            "certificado": {}
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/autofill",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            res = json.loads(resp.read().decode("utf-8"))
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
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/generate_pdf",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            res = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(res["status"], "ok")
            self.assertIn("pdf_preview_url", res)

    def test_api_ingreso_tecnico(self):
        payload = {
            "dns": "ce-yelcho.acuimatic.com",
            "clave_pc": "clave-de-prueba",
            "acceso_remoto": "",
            "observaciones": "Name 5 desasociado, llevar pilas o caja de repuesto.\nReponer stock de repuesto, sensor y caja jennic"
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/revisor/ingreso_tecnico",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            res = json.loads(resp.read().decode("utf-8"))
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
        from src.services.revisor_service import limpiar_salida_telnet
        raw = "Bienvenido al servidor de Telnet!\nEscape character is '^]'\nPancoordinator status\nVersion v2.0.2"
        clean = limpiar_salida_telnet(raw)
        self.assertNotIn("Bienvenido al servidor de Telnet!", clean)
        self.assertNotIn("Escape character", clean)
        self.assertIn("Pancoordinator status", clean)
        self.assertIn("Version v2.0.2", clean)


if __name__ == "__main__":
    unittest.main()
