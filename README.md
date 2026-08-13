# Certificado de Instalación - Guía de Instalación y Uso

Sistema de Validación y Generación Oficial de Certificados de Instalación para **Innovex Soluciones Tecnológicas**.

---

## 🚀 Requisitos e Instalación

### Requisitos del Sistema
- Sistema Operativo: Linux (Ubuntu 20.04 / 22.04 / 24.04 LTS recomendados) o cualquier distribución x86_64.
- No requiere Python ni dependencias preinstaladas cuando se utiliza el ejecutable compilado.

### Instalación Rápida
1. Descargue o copie el archivo ejecutable binario **`certificado-instalacion`** (ubicado en `dist/certificado-instalacion`).
2. Dé permisos de ejecución al archivo en la terminal:
   ```bash
   chmod +x certificado-instalacion
   ```
3. Ejecute la aplicación:
   ```bash
   ./certificado-instalacion
   ```

---

## 📂 Flujo de Trabajo y Carpeta Personal `~/evidencias_instalacion`

El sistema utiliza un flujo simplificado mediante una carpeta de entrada centralizada en el directorio personal del usuario:

### 1. Carpeta de Entrada de Evidencias (`~/evidencias_instalacion`)
- Al ejecutar la aplicación por primera vez, se crea automáticamente la carpeta:
  `~/evidencias_instalacion` (ubicada en `/home/<usuario>/evidencias_instalacion`).
- **Instrucciones para el Operador:**
  - Deposite allí las **fotografías del centro** (`.jpg`, `.jpeg`, `.png`).
  - Deposite allí la **planilla de configuración de alarmas** (`.ods` o `.xlsx`).

### 2. Uso de la Interfaz TUI
Al ejecutar `./certificado-instalacion`, se despliega el menú interactivo:
1. **Crear / Editar Certificado:**
   - Seleccione el año e ingrese el código del centro (ej. `ca-ahoni`).
2. **Completar Secciones:**
   - Navegue por las opciones (Datos Generales, Infraestructura, Acceso Remoto, Estación/Cámara, Monitoreo Abiótico, Ubicaciones y Sensores, Activación).
   - **Opción 8 (Evidencias):** Permite ver los archivos detectados en `~/evidencias_instalacion` y presionar **`L`** para **Limpiar la carpeta** cuando vaya a comenzar la instalación de un nuevo centro.
   - **Opción 9 (Configuración de Alarmas):** Presione **`C`** para cargar y procesar automáticamente la planilla de alarmas (`.ods` / `.xlsx`).
3. **Guardar y Generar PDF:**
   - Al seleccionar **`P` (Generar PDF)** o **`G` (Guardar)**, el sistema:
     - Copia automáticamente las fotos y planillas de `~/evidencias_instalacion` al archivo histórico del centro.
     - Genera la Ficha Oficial en PDF y la estructura en JSON.

---

## 📁 Ubicación de Archivos Generados

Todos los certificados procesados se archivan de manera estructurada en:

```text
storage/
└── certificados/
    └── <AÑO>/
        └── <LOCATION>/
            ├── certificado.json
            ├── certificado.pdf
            └── evidencias/
```

- **`certificado.json`**: Estructura de datos completa del certificado.
- **`certificado.pdf`**: Documento oficial formateado y paginado listo para entrega al cliente.
- **`evidencias/`**: Copia de respaldo histórica de las fotografías y planillas asociadas al centro.

---

## 🛠️ Desarrollo y Compilación (Para Administradores)

Si se desea modificar el código fuente o recompilar el ejecutable:

1. **Entorno de Desarrollo Python:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Ejecución desde Código Fuente:**
   ```bash
   python main.py
   ```
3. **Pruebas Automatizadas:**
   ```bash
   python tests/test_full_workflow.py
   ```
4. **Compilar Nuevo Ejecutable:**
   ```bash
   pyinstaller --onefile --name "certificado-instalacion" --add-data "assets:assets" main.py
   ```
   *(El binario resultante se guardará en `dist/certificado-instalacion`)*.