"""
Crea un superusuario administrador por defecto si no existe ninguno.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def main():
    username = "admin"
    email = "soporte@innovex.cl"
    password = "admin"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Superusuario '{username}' creado exitosamente con clave '{password}'.")
        print("   Puede ingresar al panel administrativo en: http://localhost:8888/admin/")
    else:
        print(f"ℹ️ El superusuario '{username}' ya existe.")


if __name__ == "__main__":
    main()
