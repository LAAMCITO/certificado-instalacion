# Estructura JSON

## Raíz Del Documento

El archivo `certificado.json` se guarda con esta estructura general:

```text
metadata
datos_generales
infraestructura
acceso_remoto
camara
estacion
antena
ubicaciones
activacion
observaciones
evidencias
```

## Descripción De Secciones

- `metadata`: información técnica interna del documento.
- `datos_generales`: identificación del certificado y del centro.
- `infraestructura`: datos de la infraestructura principal.
- `acceso_remoto`: datos de conexión para soporte remoto.
- `camara`: información de cámara, si existe.
- `estacion`: información de estación ambiental, si existe.
- `antena`: información de la antena, si existe.
- `ubicaciones`: lista de sectores donde se instalan equipos.
- `activacion`: validación realizada por soporte.
- `observaciones`: texto libre final.
- `evidencias`: referencias a archivos adjuntos.

## Ejemplo Real

```json
{
  "metadata": {
    "uuid": "ac477ec2-dc6e-4f47-bc25-5ba80118f3d7",
    "version_modelo": "1.0",
    "fecha_creacion": "2026-06-16T16:41:58.167285",
    "fecha_modificacion": "2026-06-16T16:41:58.167285"
  },
  "datos_generales": {
    "responsable": "",
    "empresa": "",
    "centro": "inn-prueba2",
    "fecha_instalacion": "",
    "tecnico_visita": "",
    "numero_ficha": ""
  },
  "infraestructura": {},
  "acceso_remoto": {},
  "camara": {},
  "estacion": {},
  "antena": {},
  "ubicaciones": [],
  "activacion": {
    "fecha_creacion_monitor": "",
    "tipo_ip": "",
    "ip_final": "",
    "ping_ok": false,
    "ssh_ok": false,
    "datos_visibles": false,
    "transmision_ok": false,
    "alarmas_activadas": false,
    "responsable_activacion": "",
    "estado_final": ""
  },
  "observaciones": "",
  "evidencias": []
}
```

## Almacenamiento

- Ruta base: `storage/certificados/`.
- Organización: año -> centro -> `certificado.json`.
- Las evidencias deben ubicarse junto al certificado dentro de su carpeta de centro.
