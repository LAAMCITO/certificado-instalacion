import socket
import socketserver
import threading
import unittest
import os

# Setup Django test environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from apps.revisor.services import RevisorService
from apps.core.utils.autofill import parse_cmd_status


class _PancoordinatorTelnetHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Simula el banner que entrega el servidor real antes del comando.
        self.request.sendall(b"Bienvenido al servidor de Telnet!\r\n")
        comando = self.request.recv(1024).decode("utf-8", errors="replace").strip()
        self.server.comandos.append(comando)

        if comando == "cmd status":
            respuesta = (
                "Pancoordinator status\r\n"
                "Version v9.3.1\r\n"
                "MAC: 00:15:8D:00:AA:BB:CC\r\n"
                "Pan ID: 4321\r\n"
                "N of motes attached: 2\r\n"
            )
        elif comando == "cmd motes":
            respuesta = "1 00:15:8D:00:00:00:01 80:81 4 Equipo 1\r\n"
        else:
            respuesta = "Comando desconocido\r\n"
        self.request.sendall(respuesta.encode("utf-8"))


class TestTelnetAutofill(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = socketserver.TCPServer(("127.0.0.1", 0), _PancoordinatorTelnetHandler)
        cls.server.comandos = []
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_autofill_usa_telnet_en_puerto_elegido_sin_ssh(self):
        salida = RevisorService.ejecutar_ssh_autofill({
            "host": "127.0.0.1",
            "puerto_telnet": str(self.port),
            # Sin clave/contrasena SSH: Telnet debe seguir funcionando.
        })

        self.assertIn("Version v9.3.1", salida)
        self.assertIn("Pan ID: 4321", salida)
        self.assertIn("cmd status", self.server.comandos)
        self.assertIn("cmd motes", self.server.comandos)

        # El texto generado conserva el formato que consume procesar_autofill.
        datos_status = parse_cmd_status(salida)
        self.assertEqual(datos_status["version"], "v9.3.1")
        self.assertEqual(datos_status["mac"], "00:15:8D:00:AA:BB:CC")
        self.assertEqual(datos_status["panid"], "4321")
        self.assertEqual(datos_status["cantidad_equipos_asociados"], "2")

    def test_autofill_no_usa_datos_de_demostracion_si_telnet_falla(self):
        # Reservar y liberar un puerto garantiza un destino local sin servidor.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.bind(("127.0.0.1", 0))
            puerto_sin_servidor = probe.getsockname()[1]

        with self.assertRaisesRegex(RuntimeError, "No se pudo consultar"):
            RevisorService.ejecutar_ssh_autofill({
                "host": "127.0.0.1",
                "puerto_telnet": str(puerto_sin_servidor),
            })


if __name__ == "__main__":
    unittest.main()
