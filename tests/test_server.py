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


if __name__ == "__main__":
    unittest.main()
