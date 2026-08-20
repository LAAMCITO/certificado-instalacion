"""
Forwarding proxy to apps.portal.services
"""

from pathlib import Path
STORAGE_DIR = Path("storage")
BITACORA_PATH = STORAGE_DIR / "bitacora.json"
DESTINATARIOS_PATH = STORAGE_DIR / "destinatarios.json"
ASISTENTES_PATH = STORAGE_DIR / "asistentes.json"

from apps.portal.services import *
