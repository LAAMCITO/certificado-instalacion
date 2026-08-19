# Suite de Soporte Innovex — Portal Unificado (Django)

Portal Web Unificado y Suite de Herramientas de Soporte Técnico para **Innovex Soluciones Tecnológicas**, desarrollado sobre **Django 5.1** y **SQLite**.

---

## 🚀 Arquitectura y Módulos

La plataforma integra los 3 módulos operativos clave de soporte técnico:

1. **Dashboard y Pizarra de Turno (Bitácora & Comunicados)**: Handover de turno en vivo, gestión de asistentes, destinatarios y generador masivo de comunicados de fin de semana con firma corporativa.
2. **Certificados de Instalación**: Validación de hardware, software, antenas Jennic, estaciones meteorológicas, cámaras PoE, sensores abióticos, planillas de alarmas y generación oficial de PDFs.
3. **Revisor de Equipos & Ingreso Técnico**: Diagnóstico remoto automatizado (SSH/Telnet), verificación de estado de enlaces y generación de plantillas de ingreso técnico.
4. **Panel de Administración Django (`/admin/`)**: Gestión visual y persistente de Asistentes, Destinatarios de Correos, Bitácora y Certificados en SQLite.

---

## 🛠️ Requisitos e Instalación

### Requisitos
- Python 3.10+ (Ubuntu 20.04 / 22.04 / 24.04 LTS o cualquier distribución Linux).

### Instalación
1. Clonar el repositorio y acceder a la carpeta:
   ```bash
   git clone https://github.com/LAAMCITO/suite-soporte-innovex.git
   cd suite-soporte-innovex
   ```
2. Crear y activar el entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Aplicar migraciones de base de datos:
   ```bash
   python manage.py migrate
   ```
5. (Opcional) Importar datos iniciales y crear administrador:
   ```bash
   python scripts/import_json_to_sqlite.py
   python scripts/create_default_admin.py
   ```

---

## 🖥️ Ejecución del Servidor

### Inicio Rápido (Recomendado)
```bash
python main.py
```
*Abre automáticamente el navegador en `http://localhost:8888/` y expone el portal en la red local para tus colegas.*

### Parámetros opcionales
```bash
python main.py --port 8000           # Puerto personalizado
python main.py --host 127.0.0.1      # Solo local
python main.py --no-browser          # Sin abrir navegador automáticamente
```

### O mediante Django CLI estándar
```bash
python manage.py runserver 0.0.0.0:8888
```

---

## 📂 Estructura del Proyecto

```text
suite-soporte-innovex/
├── manage.py                   # CLI administrativo Django
├── main.py                     # Launcher rápido con auto-detección de IPs
├── config/                     # Configuración Django (settings, urls, wsgi, asgi)
├── apps/
│   ├── core/                   # Parsers, utilidades, constantes, generador PDF
│   ├── certificados/           # CRUD Certificados, autofill, reportes PDF
│   ├── revisor/                # Verificación SSH/Telnet, plantillas técnicas
│   └── portal/                 # Bitácora, asistentes, destinatarios, correos
├── static/                     # Archivos estáticos (CSS, JS, Logos)
├── templates/                  # Templates HTML (index.html con tags Django)
├── storage/                    # Almacenamiento histórico de PDFs y evidencias
├── db.sqlite3                  # Base de datos SQLite
└── tests/                      # Suite de pruebas automatizadas (36 tests)
```

---

## 🧪 Pruebas Automatizadas

Para ejecutar la suite completa de 36 pruebas unitarias:
```bash
python manage.py test tests
```
O con unittest:
```bash
python -m unittest discover tests
```