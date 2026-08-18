from src.utils.autofill import procesar_autofill, parse_cacheton_json

def test_cacheton_config_json_parsing():
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
    # 1. Test parse_cacheton_json direct parsing
    parsed = parse_cacheton_json(json_texto)
    assert parsed.get("puerto_server") == "8888", f"Esperado '8888', obtenido '{parsed.get('puerto_server')}'"
    assert parsed.get("hostserver") == "dataweb.innovex.cl", f"Esperado 'dataweb.innovex.cl', obtenido '{parsed.get('hostserver')}'"
    assert parsed.get("location") == "ce-tranqui1", f"Esperado 'ce-tranqui1', obtenido '{parsed.get('location')}'"

    # 2. Test procesar_autofill into certificate dict
    cert = {}
    res = procesar_autofill(cert, json_texto)
    puerto_obtenido = cert.get("acceso_remoto", {}).get("puerto_server")
    host_obtenido = cert.get("acceso_remoto", {}).get("hostserver")

    assert puerto_obtenido == "8888", f"Esperado puerto '8888', pero en el certificado quedó '{puerto_obtenido}'"
    assert host_obtenido == "dataweb.innovex.cl", f"Esperado host 'dataweb.innovex.cl', obtenido '{host_obtenido}'"
    print("✅ test_cacheton_config_json_parsing PASSED!")


def test_pegar_alarmas_texto():
    from src.utils.excel_parser import parsear_alarmas_texto

    texto_alarmas = """Estado 	Usuario 	Mínima 	Máxima 	Medicion Especifica 	Centros 	Equipo 	Sensor 	Acción
Activo 	ac-centro.yatac 	4,5 	16,0 		(3583) Yatac - Aquachile 	Equipo 1 	(27943) Sensor 5 mts Pontón - Oxygen (oxygen) - Yatac (ac-yatac) 	
Activo 	ac-rodrigo.garcia 	4,5 	16,0 		(3583) Yatac - Aquachile 	Equipo 1 	(27943) Sensor 5 mts Pontón - Oxygen (oxygen) - Yatac (ac-yatac) 	
Activo 	edwin 	4,5 	16,0 		(3583) Yatac - Aquachile 	Equipo 2 	(27944) Sensor 10 mts Pontón - Oxygen (oxygen) - Yatac (ac-yatac) 	
"""
    alarmas = parsear_alarmas_texto(texto_alarmas)
    assert len(alarmas) == 3, f"Esperado 3 alarmas, obtenido {len(alarmas)}"
    assert alarmas[0]["correo"] == "ac-centro.yatac"
    assert alarmas[0]["equipo"] == "Equipo 1"
    assert alarmas[0]["conf_min"] == "4,5"
    assert alarmas[0]["conf_max"] == "16,0"
    assert alarmas[0]["medicion"] == "Oxígeno"
    assert alarmas[2]["equipo"] == "Equipo 2"
    print("✅ test_pegar_alarmas_texto PASSED!")


def test_incremental_autofill_preserves_data():
    cert = {}

    # Paso 1: Parsear cmd status
    txt1 = "Version v2.0.2\nMAC: 00:15:8D:00:09:24:53:F7\nPAN ID: 2020"
    procesar_autofill(cert, txt1)
    assert cert["monitoreo_abiotico"]["version"] == "v2.0.2"

    # Paso 2: Parsear cmd motes (debe mantener monitoreo_abiotico)
    txt2 = "1 00:15:8D:00:09:24:53:F8 -75dBm 2s 9"
    procesar_autofill(cert, txt2)
    assert cert["monitoreo_abiotico"]["version"] == "v2.0.2"
    assert len(cert["motes"]) == 2

    # Paso 3: Parsear alarmas en texto (debe mantener monitoreo_abiotico y motes)
    txt3 = "Estado\tUsuario\tMínima\tMáxima\tMedicion\tCentros\tEquipo\tSensor\nActivo\tadmin\t4.0\t15.0\tOxygen\tYatac\tEquipo 1\tSensor 1"
    procesar_autofill(cert, txt3)
    assert cert["monitoreo_abiotico"]["version"] == "v2.0.2"
    assert len(cert["motes"]) == 2
    assert len(cert["configuracion_alarmas"]) == 1

    print("✅ test_incremental_autofill_preserves_data PASSED!")


def test_eliminar_certificado():
    from src.services.certificado_service import CertificadoService
    location = "test_del_loc"
    año = 2026

    # Guardar certificado de prueba
    CertificadoService.guardar_certificado({"datos_generales": {"location": location}}, location, año)
    assert location in CertificadoService.listar_certificados(año)

    # Eliminar certificado
    exito = CertificadoService.eliminar_certificado(location, año)
    assert exito is True
    assert location not in CertificadoService.listar_certificados(año)

    print("✅ test_eliminar_certificado PASSED!")


def test_parse_kernel_and_hostnamectl_autofill():
    from src.utils.autofill import procesar_autofill
    cert = {}
    txt = """
    Static hostname: ce-llancacheo
    Operating System: Ubuntu 20.04.6 LTS
    Kernel: Linux 5.15.0-134-generic
    """
    res = procesar_autofill(cert, txt)
    assert res["exito"] is True
    assert cert["datos_generales"]["location"] == "ce-llancacheo"
    assert cert["infraestructura"]["sistema_operativo"] == "Ubuntu 20.04.6 LTS"
    assert cert["infraestructura"]["kernel"] == "5.15.0-134-generic"
    print("✅ test_parse_kernel_and_hostnamectl_autofill PASSED!")


if __name__ == "__main__":
    test_cacheton_config_json_parsing()
    test_pegar_alarmas_texto()
    test_incremental_autofill_preserves_data()
    test_eliminar_certificado()
    test_parse_kernel_and_hostnamectl_autofill()
