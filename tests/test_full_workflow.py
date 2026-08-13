from pathlib import Path
from PIL import Image, ImageDraw
from src.services.certificado_service import CertificadoService
from src.pdf.generador_pdf import GeneradorPDF
from src.utils.whatsapp_parser import parsear_mensaje_whatsapp


def crear_imagenes_muestra(dir_evidencias: Path):
    dir_evidencias.mkdir(parents=True, exist_ok=True)

    # Nombres de archivos aleatorios tipo WhatsApp
    muestras = [
        ("IMG-20260804-WA0001.jpg", (30, 40, 50), "Fotografía Computador"),
        ("IMG-20260804-WA0002.jpg", (40, 70, 90), "Fotografía Antena"),
        ("IMG-20260804-WA0003.jpg", (60, 90, 60), "Fotografía Estación Meteo"),
        ("IMG-20260804-WA0004.jpg", (90, 60, 40), "Fotografía Sensores")
    ]

    for nombre, col, titulo in muestras:
        ruta_img = dir_evidencias / nombre
        if not ruta_img.exists():
            img = Image.new('RGB', (800, 600), color=col)
            draw = ImageDraw.Draw(img)
            draw.rectangle([30, 30, 770, 570], outline=(255, 255, 255), width=4)
            draw.text((50, 280), f"INNOVEX - {titulo}", fill=(255, 255, 255))
            img.save(ruta_img)


def test_full_workflow():
    # Mensaje semi-informal recibido del técnico vía WhatsApp
    mensaje_whatsapp_tecnico = """
Colegas, Instalación finalizada en ca-ahoni
Solo se instala 1 módulo ya que el otro aún no está listo me informan que en aproximadamente 2 semanas ya estaría en condiciones de poderse instalar, por distancia se recomienda instalar otro pc similar a la instalación de pilpilehue 
Datos del centro los comparto más tarde 
favor activar monitor
Location: ca-ahoni 
Port server: 8.8.8.8
Tun 0:  10.9.6.109
Clave: CAMANCHACA@XXIV
Tipo de red: LAN
Puerto patron: isla lemuy
Coordenadas: -42.749224 -73.580710
Barrio: 10A
Artefacto naval: CAMANCHACA XXIV

Pontón -42.749224 -73.580710

name 1: prof. 5mts / Parametro: oxi-sal-t° 
name 2: prof. 10 mts / Parametro: oxi-sal-t°

Jaula : 205
Coordenadas: -42.749734 -73.582706
name 3: prof. 5 mts / Parametro: oxi-sal-t° 
name 4: prof. 10 mts / Parametro: oxi-sal-t°
name 5: prof. 15 mts / Parametro: oxi-sal-t° 
name 6: prof. 20 mts / Parametro: oxi-sal-t°
"""

    # 1. Parsear el mensaje técnico automáticamente
    parsed_data = parsear_mensaje_whatsapp(mensaje_whatsapp_tecnico)
    location = parsed_data["datos_generales"]["location"]
    año = 2026

    # Asignar número de ficha de prueba (generará Registro: cer-9653)
    parsed_data["datos_generales"]["numero_ficha"] = "9653"

    # Directorio estándar de evidencias oficial
    dir_evidencias = CertificadoService.obtener_carpeta_evidencias(location, año)
    crear_imagenes_muestra(dir_evidencias)

    # 2. Crear instancia del objeto Certificado
    certificado_obj = CertificadoService.crear_certificado(
        location=location,
        nombre_centro=parsed_data["datos_generales"]["nombre_centro"]
    )

    certificado_obj.datos_generales.update(parsed_data["datos_generales"])
    certificado_obj.infraestructura.update(parsed_data["infraestructura"])
    certificado_obj.acceso_remoto.update(parsed_data["acceso_remoto"])
    certificado_obj.ubicaciones = parsed_data["ubicaciones"]
    certificado_obj.equipos_repuesto = parsed_data.get("equipos_repuesto", [])
    certificado_obj.observaciones = parsed_data["observaciones"]

    # 3. Guardar JSON
    ruta_json = CertificadoService.guardar_certificado(
        certificado=certificado_obj,
        location=location,
        año=año
    )
    print(f"Certificado JSON guardado en: {ruta_json}")

    # 4. Generar PDF (Ficha Oficial Innovex con Registro: cer-9653)
    base_dir = Path("storage/certificados") / str(año) / location
    ruta_pdf = base_dir / f"certificado_inst_{location}.pdf"
    GeneradorPDF().generar(parsed_data, str(ruta_pdf), carpeta_evidencias=dir_evidencias)
    print(f"Certificado PDF generado en: {ruta_pdf}")


if __name__ == "__main__":
    test_full_workflow()
