"""
Entry point for Suite de Soporte Innovex (Django backend).
"""

import os
import sys
import socket
import webbrowser
from pathlib import Path
import threading
import time

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def obtener_ips_locales() -> list[str]:
    """Retorna las direcciones IPv4 locales de las interfaces de red activas."""
    ips = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_principal = s.getsockname()[0]
        s.close()
        if ip_principal and not ip_principal.startswith("127."):
            ips.append(ip_principal)
    except Exception:
        pass

    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith("127.") and ip not in ips:
                ips.append(ip)
    except Exception:
        pass

    return ips


def abrir_navegador_delayed(url: str, delay: float = 1.0):
    def _open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
        except Exception:
            pass
    threading.Thread(target=_open, daemon=True).start()


def main():
    args = sys.argv[1:]
    puerto_solicitado = 8888
    host_solicitado = "0.0.0.0"

    for i, arg in enumerate(args):
        if (arg == "--port" or arg == "-p") and i + 1 < len(args):
            try:
                puerto_solicitado = int(args[i + 1])
            except ValueError:
                pass
        elif (arg == "--host" or arg == "-h") and i + 1 < len(args):
            host_solicitado = args[i + 1]
        elif arg == "--local" or arg == "--localhost":
            host_solicitado = "127.0.0.1"

    # Verificar disponibilidad de puerto
    while puerto_solicitado < 8910:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host_solicitado if host_solicitado != "0.0.0.0" else "", puerto_solicitado))
                break
            except OSError:
                puerto_solicitado += 1

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    ips = obtener_ips_locales()
    url_local = f"http://localhost:{puerto_solicitado}/"

    print("=" * 65)
    print("  SUITE DE SOPORTE INNOVEX — PORTAL UNIFICADO (DJANGO)")
    print("=" * 65)
    print(f"🚀 Servidor Django activo en el puerto {puerto_solicitado}:")
    print(f"   • Local (este equipo):  {url_local}")
    if host_solicitado in ("0.0.0.0", ""):
        if ips:
            for ip in ips:
                print(f"   • Red Local (colegas):  http://{ip}:{puerto_solicitado}/")
        else:
            print(f"   • Red Local (colegas):  http://<IP-de-tu-equipo>:{puerto_solicitado}/")
    else:
        print(f"   • Host específico:      http://{host_solicitado}:{puerto_solicitado}/")
    print(f"   • Panel de Administración: {url_local}admin/")
    print("  💡 Presione Ctrl+C en esta terminal para detener el servidor.")
    print("=" * 65)

    # Abrir navegador si no se pasa --no-browser
    if "--no-browser" not in args:
        abrir_navegador_delayed(url_local, delay=1.2)

    # Ejecutar Django runserver
    from django.core.management import execute_from_command_line
    django_args = [
        "manage.py",
        "runserver",
        f"{host_solicitado}:{puerto_solicitado}",
    ]
    if "--noreload" in args:
        django_args.append("--noreload")
    execute_from_command_line(django_args)


if __name__ == "__main__":
    main()