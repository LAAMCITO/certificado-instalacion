"""
Script para importar datos existentes desde storage/*.json a SQLite.
"""

import os
import sys
import json
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from apps.portal.models import Asistente, Destinatario, Bitacora
from apps.certificados.models import CertificadoInstalacion

STORAGE_DIR = BASE_DIR / "storage"


def importar_asistentes():
    path = STORAGE_DIR / "asistentes.json"
    if not path.exists():
        print("ℹ️ No se encontró asistentes.json")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    count = 0
    for idx, item in enumerate(data, start=1):
        _, created = Asistente.objects.update_or_create(
            correo=item["correo"],
            defaults={
                "nombre": item["nombre"],
                "cargo": item.get("cargo", "ASISTENTE DE SOPORTE"),
                "telefono": item.get("telefono", ""),
                "activo": item.get("activo", True),
                "orden": idx,
            }
        )
        if created:
            count += 1
    print(f"✅ Asistentes importados/actualizados: {len(data)} (nuevos: {count})")


def importar_destinatarios():
    path = STORAGE_DIR / "destinatarios.json"
    if not path.exists():
        print("ℹ️ No se encontró destinatarios.json")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    count = 0
    for item in data:
        _, created = Destinatario.objects.update_or_create(
            empresa=item["empresa"],
            correo=item["correo"],
            defaults={"activo": item.get("activo", True)}
        )
        if created:
            count += 1
    print(f"✅ Destinatarios importados/actualizados: {len(data)} (nuevos: {count})")


def importar_bitacora():
    path = STORAGE_DIR / "bitacora.json"
    if not path.exists():
        print("ℹ️ No se encontró bitacora.json")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    texto = data.get("texto", "")
    bitacora = Bitacora.objects.first()
    if not bitacora:
        Bitacora.objects.create(texto=texto)
    else:
        bitacora.texto = texto
        bitacora.save()
    print("✅ Bitácora importada correctamente")


def importar_certificados():
    dir_certs = STORAGE_DIR / "certificados"
    if not dir_certs.exists():
        print("ℹ️ No se encontró storage/certificados")
        return
    count = 0
    for año_dir in dir_certs.iterdir():
        if not año_dir.is_dir() or not año_dir.name.isdigit():
            continue
        año = int(año_dir.name)
        for loc_dir in año_dir.iterdir():
            if not loc_dir.is_dir():
                continue
            json_file = loc_dir / "certificado.json"
            if json_file.exists():
                try:
                    data = json.loads(json_file.read_text(encoding="utf-8"))
                    dg = data.get("datos_generales", {})
                    loc = dg.get("location") or loc_dir.name
                    CertificadoInstalacion.objects.update_or_create(
                        location=loc,
                        año=año,
                        defaults={
                            "nombre_centro": dg.get("nombre_centro", ""),
                            "empresa": dg.get("empresa", ""),
                            "fecha_instalacion": dg.get("fecha_instalacion", ""),
                            "tecnico_visita": dg.get("tecnico_visita", ""),
                            "numero_ficha": dg.get("numero_ficha", ""),
                            "data": data,
                        }
                    )
                    count += 1
                except Exception as exc:
                    print(f"⚠️ Error importando certificado {loc_dir}: {exc}")
    print(f"✅ Certificados históricos importados a SQLite: {count}")


def main():
    print("🚀 Iniciando importación de datos a SQLite...")
    importar_asistentes()
    importar_destinatarios()
    importar_bitacora()
    importar_certificados()
    print("🎉 Importación completada con éxito.")


if __name__ == "__main__":
    main()
