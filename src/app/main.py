import sys
import webbrowser
import time
from pathlib import Path

# Asegurar que la raíz del proyecto esté en sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.server.server import iniciar_servidor_http
from src.tui.menu import Menu


def main():
    args = sys.argv[1:]
    
    if "--consola" in args or "-c" in args or "--tui" in args:
        print("🖥️ Iniciando en modo Consola Terminal (TUI)...")
        menu = Menu()
        menu.mostrar()
        return

    # Modo Servidor Web Live (Default)
    puerto_solicitado = 8888
    for i, arg in enumerate(args):
        if (arg == "--port" or arg == "-p") and i + 1 < len(args):
            try:
                puerto_solicitado = int(args[i + 1])
            except ValueError:
                pass

    server, puerto = iniciar_servidor_http(host="127.0.0.1", puerto=puerto_solicitado)
    url = f"http://127.0.0.1:{puerto}/"
    
    print("=" * 65)
    print("  CERTIFICADO DE INSTALACIÓN — EDICIÓN Y VISTA PREVIA EN VIVO")
    print("=" * 65)
    print(f"  🌐 Abriendo navegador web en: {url}")
    print("  💡 Presione Ctrl+C en esta terminal para detener el servidor.")
    print("  🖥️ Para usar el modo terminal ejecute: ./certificado-instalacion-live --consola")
    print("=" * 65)

    try:
        webbrowser.open(url)
    except Exception:
        print(f"No se pudo abrir automáticamente el navegador. Ingrese a: {url}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor web... ¡Hasta luego!")
        server.server_close()


if __name__ == "__main__":
    main()