import os
import unittest

# Setup Django test environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from apps.core.utils.autofill import procesar_autofill, parse_cacheton_json, parse_cmd_status
from apps.core.utils.excel_parser import parsear_alarmas_texto
from apps.core.utils.motes_parser import parse_cmd_motes
from apps.certificados.services import CertificadoService


class TestAutofillJSON(unittest.TestCase):

    def test_cacheton_config_json_parsing(self):
        json_texto = """
innovex@ce-tranqui1:~$ cat /etc/cacheton/config_location.json
{
    "location": "ce-tranqui1",
    "source": "/var/lib/cacheton/data",
    "hostlocal": "localhost",
    "portlocal": 8888,
    "hostserver": "dataweb.innovex.cl",
    "portserver": 8888,
    "device": "/dev/serial/by-id/usb-INNOVEX_INNOVEX_FTFMF3LN-if00-port0",
    "baudrate": "115200",
    "dev_multi": "",
    "baud_multi": "",
    "dev_weather": "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10MX896-if00-port0",
    "baud_weather": 4800,
    "interval_weather": 300,
    "hostserver_weather": "desarrollo.innovex.cl",
    "portserver_weather": "8989",
    "logfile": "/var/log/cacheton/jenreceiver.log",
    "thread": 10,
    "tag": "/cacheton",
    "unixtime": "no"
}
"""
        parsed = parse_cacheton_json(json_texto)
        self.assertEqual(parsed.get("puerto_server"), "8888")
        self.assertEqual(parsed.get("hostserver"), "dataweb.innovex.cl")
        self.assertEqual(parsed.get("location"), "ce-tranqui1")

        cert = {}
        procesar_autofill(cert, json_texto)
        self.assertEqual(cert.get("acceso_remoto", {}).get("puerto_server"), "8888")
        self.assertEqual(cert.get("acceso_remoto", {}).get("hostserver"), "dataweb.innovex.cl")

    def test_pegar_alarmas_texto(self):
        texto_alarmas = """Estado 	Usuario 	Mínima 	Máxima 	Medicion Especifica 	Centros 	Equipo 	Sensor 	Acción
Activo 	ac-centro.yatac 	4,5 	16,0 		(3583) Yatac - Aquachile 	Equipo 1 	(27943) Sensor 5 mts Pontón - Oxygen (oxygen) - Yatac (ac-yatac) 	
Activo 	ac-rodrigo.garcia 	4,5 	16,0 		(3583) Yatac - Aquachile 	Equipo 1 	(27943) Sensor 5 mts Pontón - Oxygen (oxygen) - Yatac (ac-yatac) 	
Activo 	edwin 	4,5 	16,0 		(3583) Yatac - Aquachile 	Equipo 2 	(27944) Sensor 10 mts Pontón - Oxygen (oxygen) - Yatac (ac-yatac) 	
"""
        alarmas = parsear_alarmas_texto(texto_alarmas)
        self.assertEqual(len(alarmas), 3)
        self.assertEqual(alarmas[0]["correo"], "ac-centro.yatac")
        self.assertEqual(alarmas[0]["equipo"], "Equipo 1")
        self.assertEqual(alarmas[0]["conf_min"], "4,5")
        self.assertEqual(alarmas[0]["conf_max"], "16,0")
        self.assertEqual(alarmas[0]["medicion"], "Oxígeno")
        self.assertEqual(alarmas[2]["equipo"], "Equipo 2")

    def test_incremental_autofill_preserves_data(self):
        cert = {}

        # Paso 1: Parsear cmd status
        txt1 = "Version v2.0.2\nMAC: 00:15:8D:00:09:24:53:F7\nPAN ID: 2020"
        procesar_autofill(cert, txt1)
        self.assertEqual(cert["monitoreo_abiotico"]["version"], "v2.0.2")

        # Paso 2: Parsear cmd motes
        txt2 = "1 00:15:8D:00:09:24:53:F8 -75dBm 2s 9"
        procesar_autofill(cert, txt2)
        self.assertEqual(cert["monitoreo_abiotico"]["version"], "v2.0.2")
        self.assertEqual(len(cert["motes"]), 2)

        # Paso 3: Parsear alarmas en texto
        txt3 = "Estado\tUsuario\tMínima\tMáxima\tMedicion\tCentros\tEquipo\tSensor\nActivo\tadmin\t4.0\t15.0\tOxygen\tYatac\tEquipo 1\tSensor 1"
        procesar_autofill(cert, txt3)
        self.assertEqual(cert["monitoreo_abiotico"]["version"], "v2.0.2")
        self.assertEqual(len(cert["motes"]), 2)
        self.assertEqual(len(cert["configuracion_alarmas"]), 1)

    def test_eliminar_certificado(self):
        location = "test_del_loc"
        año = 2026

        CertificadoService.guardar_certificado({"datos_generales": {"location": location}}, location, año)
        self.assertIn(location, CertificadoService.listar_certificados(año))

        exito = CertificadoService.eliminar_certificado(location, año)
        self.assertTrue(exito)
        self.assertNotIn(location, CertificadoService.listar_certificados(año))

    def test_parse_kernel_and_hostnamectl_autofill(self):
        cert = {}
        txt = """
        Static hostname: ce-llancacheo
        Operating System: Ubuntu 20.04.6 LTS
        Kernel: Linux 5.15.0-134-generic
        """
        res = procesar_autofill(cert, txt)
        self.assertTrue(res["exito"])
        self.assertEqual(cert["datos_generales"]["location"], "ce-llancacheo")
        self.assertEqual(cert["infraestructura"]["sistema_operativo"], "Ubuntu 20.04.6 LTS")
        self.assertEqual(cert["infraestructura"]["kernel"], "5.15.0-134-generic")

    def test_robust_cmd_status_and_motes_parsing(self):
        txt_status = """
        pancoordinator> cmd status
        Firmware Version : v2.0.4
        Coordinator MAC : 00-15-8d-00-00-5f-e3-10
        PAN ID : 0x1234
        Channel : 19
        N of motes attached : 5
        """
        st = parse_cmd_status(txt_status)
        self.assertEqual(st.get("version"), "v2.0.4")
        self.assertEqual(st.get("mac"), "00:15:8D:00:00:5F:E3:10")
        self.assertEqual(st.get("panid"), "0x1234")
        self.assertEqual(st.get("canal"), "19")
        self.assertEqual(st.get("cantidad_equipos_asociados"), "5")

        txt_motes = """
        cmd> motes
        Mote MAC Signal Last RX Name
        1 00:15:8D:00:00:23:45:67 114:120 12s Jaula 1
        2 00158d0000234568 -75dBm 4s Jaula 2
        3 00-15-8D-00-00-23-45-69 110/120 0:15 3
        [4] 00:15:8D:00:00:23:45:6A 115:120 5s MALO
        """
        motes = parse_cmd_motes(txt_motes)
        self.assertEqual(len(motes), 4)
        self.assertEqual(motes[0]["mac"], "00:15:8D:00:00:23:45:67")
        self.assertEqual(motes[0]["asociacion"], "Jaula 1")
        self.assertEqual(motes[1]["mac"], "00:15:8D:00:00:23:45:68")
        self.assertEqual(motes[1]["signal"], "-75dBm")
        self.assertEqual(motes[2]["mac"], "00:15:8D:00:00:23:45:69")
        self.assertEqual(motes[2]["asociacion"], "Equipo 3")
        self.assertEqual(motes[3]["mac"], "00:15:8D:00:00:23:45:6A")
        self.assertEqual(motes[3]["asociacion"], "MALO")

    def test_autofill_new_center_overwrites_old_center(self):
        cert = {
            "datos_generales": {
                "location": "ce-tranqui1",
                "nombre_centro": "Tranqui 1",
                "empresa": "Cermaq"
            }
        }
        nuevo_txt = """
        Static hostname: ce-unicorniosur
        Operating System: Ubuntu 22.04.4 LTS
        Kernel: Linux 5.15.0-105-generic
        """
        procesar_autofill(cert, nuevo_txt)
        self.assertEqual(cert["datos_generales"]["location"], "ce-unicorniosur")
        self.assertEqual(cert["datos_generales"]["nombre_centro"], "Unicornio Sur")
        self.assertEqual(cert["datos_generales"]["empresa"], "Cermaq")


if __name__ == "__main__":
    unittest.main()
