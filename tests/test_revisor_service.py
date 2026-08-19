import os
import unittest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from apps.revisor.services import (
    parsear_paquetes,
    parsear_so_y_kernel,
    parsear_senal_motes,
    parsear_voltaje_minimo,
    RevisorService
)


class TestRevisorService(unittest.TestCase):

    def test_parsear_paquetes(self):
        sample_log = """
=== HG PAQUETERIA ===
--- cacheton ---
changeset:   631:2f3f120577b9
tag:         tip
user:        innovex
--- python3_cacheton ---
changeset:   415:1a2b3c4d5e6f
--- pcinnovex ---
changeset:   387:998877665544
=== LS OPT SOFTWARE ===
weather-station-davis_1.1.1_amd64.deb
visibility-cam_3.6.tar.xz
        """
        paquetes = parsear_paquetes(sample_log)
        self.assertEqual(paquetes["pcinnovex"], "changeset:   387")
        self.assertEqual(paquetes["cacheton"], "changeset:   631")
        self.assertEqual(paquetes["python3_cacheton"], "changeset:   415")
        self.assertEqual(paquetes["weather_davis"], "1.1.1")
        self.assertEqual(paquetes["visibility_cam"], "3.6")

    def test_parsear_so_y_kernel(self):
        sample_log = """
=== OS_RELEASE ===
PRETTY_NAME="Ubuntu 20.04.6 LTS"
NAME="Ubuntu"
VERSION_ID="20.04"
--- KERNEL ---
5.4.0-105-generic
        """
        so, kernel = parsear_so_y_kernel(sample_log)
        self.assertEqual(so, "Linux Ubuntu 20.04.6 LTS")
        self.assertEqual(kernel, "5.4.0-105-generic")

    def test_parsear_senal_motes(self):
        motes = {
            1: {"signal": "84:90"},
            2: {"signal": "84:84"},
            3: {"signal": "78:75"},
            4: {"signal": "57:198"},
            5: {"signal": "60:66"}
        }
        # Menor yy es 66 con xx=60
        senal = parsear_senal_motes(motes)
        self.assertEqual(senal, "igual o mayor a 60/66")

    def test_parsear_voltaje_minimo(self):
        voltajes = {
            1: {"voltaje": 3.45},
            2: {"voltaje": 3.28},
            3: {"voltaje": 3.33}
        }
        v_min = parsear_voltaje_minimo(voltajes)
        self.assertEqual(v_min, "igual o mayor a 3.28V")

    def test_generar_plantilla_texto_completa(self):
        datos = {
            "centro": "CE-AULEN",
            "tipo_conexion": "Wifi",
            "sistema_operativo": "Linux Ubuntu 20.04 LTS",
            "kernel": "5.4.0-105-generic",
            "clave_pc": "mi_clave_secreta",
            "dataweb": "Ok",
            "pcinnovex": "changeset:   387",
            "cacheton": "changeset:   631",
            "python3_cacheton": "changeset:   415",
            "weather_davis": "1.1.1",
            "visibility_cam": "3.6",
            "version_equipos": "v2.0.2",
            "senal": "igual o mayor a 57/198",
            "voltajes": "igual o mayor a 3.28V",
            "saturacion": "OK",
            "salinidad": "OK",
            "temperatura": "OK",
            "camara_estado": "OK",
            "estacion_estado": "OK",
            "repuesto_equipo": "OK",
            "repuesto_sensor": "OK",
            "repuesto_kit": "OK",
            "telefono": "987654321",
            "correo": "centro@innovex.cl",
            "observaciones": "Operativo sin novedades"
        }
        plantilla = RevisorService.generar_plantilla_texto(datos)
        self.assertIn("VERIFICACIÓN INGRESO  CE-AULEN", plantilla)
        self.assertIn("* Clave: mi_clave_secreta", plantilla)
        self.assertIn("* pcinnovex: changeset:   387", plantilla)
        self.assertIn("7. Repuesto:", plantilla)
        self.assertIn("* Equipo: OK", plantilla)
        self.assertIn("* Sensor: OK", plantilla)
        self.assertIn("* Kit de limpieza: OK", plantilla)
        self.assertIn("- Operativo sin novedades", plantilla)

    def test_parsear_voltajes_y_sensores_tramas(self):
        from src.services.revisor_service import parsear_voltajes_y_sensores
        sample_log = """
        2026-08-18 16:05:36,815 DEBUG Received: :2439312:13:0:NODE 0 3.330 4.930 19.0 99 69 6.00 9.00 0 0
        2026-08-18 16:05:37,100 DEBUG Received: :2439313:1:0:NODE 0 3.250 4.880 19.0 99 69 6.00 9.00 0 0
        :2:0:NODE 0 3.180 4.850 19.0 99 69 6.00 9.00 0 0
        :2:0:OXY 0 10.00 12.76 8.97 96.1 20.00 0 6 0 13 0 6
        :2:1:COND 0 10.00 12.72 35.67 46.67 32.13 0 6 0 0 13 13
        :1:0:FLOW 0 10.00 -84.18 5.19 205.00 9 0 0 0 0
        """
        voltajes, sensores = parsear_voltajes_y_sensores(sample_log)
        self.assertEqual(voltajes[13]["voltaje"], 3.33)
        self.assertEqual(voltajes[1]["voltaje"], 3.25)
        self.assertEqual(voltajes[2]["voltaje"], 3.18)

        self.assertIn("oxy", sensores[2])
        self.assertEqual(sensores[2]["oxy"]["sat"], 96.1)
        self.assertEqual(sensores[2]["oxy"]["o2"], 8.97)
        self.assertEqual(sensores[2]["oxy"]["temp"], 12.76)

        self.assertIn("cond", sensores[2])
        self.assertEqual(sensores[2]["cond"]["sal"], 32.13)

        self.assertIn("flow", sensores[1])
        self.assertEqual(sensores[1]["flow"]["vel"], 5.19)
        self.assertEqual(sensores[1]["flow"]["dir"], 205.0)

    def test_parsear_kernel_hostnamectl(self):
        sample_hostnamectl = """
   Static hostname: ce-llancacheo
         Icon name: computer-laptop
           Chassis: laptop
        Machine ID: 4e39d3611a3a41c7a007a59c37d5bab7
           Boot ID: a899ef6d41c84c06a2b0cf501072aca1
  Operating System: Ubuntu 20.04.6 LTS
            Kernel: Linux 5.15.0-134-generic
      Architecture: x86-64
        """
        so, kernel = parsear_so_y_kernel(sample_hostnamectl)
        self.assertEqual(so, "Linux Ubuntu 20.04.6 LTS")
        self.assertEqual(kernel, "5.15.0-134-generic")


    def test_parsear_paquetes_sin_dependencias(self):
        log_vacio = "=== HG PAQUETERIA ===\n=== LS OPT SOFTWARE ==="
        paquetes = parsear_paquetes(log_vacio)
        self.assertEqual(paquetes["weather_davis"], "N/A")
        self.assertEqual(paquetes["visibility_cam"], "N/A")
        self.assertEqual(paquetes["pcinnovex"], "N/A")
        self.assertEqual(paquetes["cacheton"], "N/A")

    def test_parsear_voltaje_minimo_vacio(self):
        self.assertEqual(parsear_voltaje_minimo({}), "N/A")

    def test_centro_titulo_no_forzar_ce(self):
        datos = {
            "centro": "sc-acopiocululil",
            "tipo_conexion": "Wifi",
            "sistema_operativo": "Linux Ubuntu 20.04 LTS",
            "kernel": "5.15.0-134-generic",
            "clave_pc": "SC@Acululil",
            "dataweb": "Ok",
            "weather_davis": "N/A",
            "visibility_cam": "N/A",
            "voltajes": "N/A"
        }
        plantilla = RevisorService.generar_plantilla_texto(datos)
        self.assertIn("VERIFICACIÓN INGRESO  SC-ACOPIO CULULIL", plantilla)
        self.assertNotIn("CE-SC-ACOPIO", plantilla)
        self.assertIn("* Weather Davis: N/A", plantilla)
        self.assertIn("* Visibility-cam: N/A", plantilla)
        self.assertIn("* Voltajes: N/A", plantilla)


    def test_parsear_so_y_kernel_ubuntu_24_modern(self):
        sample_hostnamectl = """
 Static hostname: sc-acopiocululil
       Icon name: computer-laptop
         Chassis: laptop 💻
      Machine ID: 953aba5775f645459986d61f59b189cb
         Boot ID: 85560e20661d42b5980d5d26add415c7
Operating System: Ubuntu 24.04.4 LTS              
          Kernel: Linux 7.0.0-29-generic
    Architecture: x86-64
 Hardware Vendor: Dell Inc.
  Hardware Model: Vostro 3400
Firmware Version: 1.5.0
   Firmware Date: Tue 2021-04-27
    Firmware Age: 5y 3month 3w 2d
        """
        so, kernel = parsear_so_y_kernel(sample_hostnamectl)
        self.assertEqual(so, "Linux Ubuntu 24.04.4 LTS")
        self.assertEqual(kernel, "7.0.0-29-generic")

    def test_parsear_voltajes_epoch_timestamp(self):
        sample_log = """
2026-08-19 13:31:18,951 DEBUG    Received: :1787160667:1:0:NODE 0 3.320 4.930 21.0 111 46 6.00 9.00 1 0
2026-08-19 13:33:36,573 DEBUG    Received: :1787160797:20:0:NODE 0 3.320 4.930 23.0 117 67 6.00 9.00 1 0
2026-08-19 13:35:22,472 DEBUG    Received: :1787160909:2:0:NODE 0 3.330 4.930 22.0 78 52 6.00 9.00 1 0
2026-08-19 13:36:33,894 DEBUG    Received: :1787160981:1:0:NODE 0 3.310 4.930 21.0 114 -3 6.00 9.00 1 0
        """
        from src.services.revisor_service import parsear_voltajes_y_sensores, parsear_tipo_conexion
        voltajes, sensores = parsear_voltajes_y_sensores(sample_log)
        self.assertIn(1, voltajes)
        self.assertEqual(voltajes[1]["voltaje"], 3.31)
        self.assertIn(20, voltajes)
        self.assertEqual(voltajes[20]["voltaje"], 3.32)
        self.assertIn(2, voltajes)
        self.assertEqual(voltajes[2]["voltaje"], 3.33)

        volt_min = parsear_voltaje_minimo(voltajes)
        self.assertEqual(volt_min, "igual o mayor a 3.31V")

    def test_parsear_tipo_conexion_cableada(self):
        from src.services.revisor_service import parsear_tipo_conexion
        sample_ip_a = """
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
2: enp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 10.150.20.14/24 brd 10.150.20.255 scope global dynamic noprefixroute enp2s0
3: wlp3s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
        """
        tipo = parsear_tipo_conexion(sample_ip_a)
        self.assertEqual(tipo, "Cableada")

    def test_parsear_tipo_conexion_wifi(self):
        from src.services.revisor_service import parsear_tipo_conexion
        sample_ip_a = """
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    inet 192.168.1.50/24 brd 192.168.1.255 scope global dynamic noprefixroute wlan0
        """
        tipo = parsear_tipo_conexion(sample_ip_a)
        self.assertEqual(tipo, "Wifi")


if __name__ == "__main__":
    unittest.main()

