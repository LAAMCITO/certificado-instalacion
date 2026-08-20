# Modelo De Datos

## Objetivo

Registrar de forma estandarizada la información de instalación y activación de un centro, manteniendo un respaldo interno útil para soporte, operaciones y revisiones futuras.

## Estructura Conceptual

```text
Certificado
├── metadata
├── datos_generales
├── infraestructura
├── acceso_remoto
├── cámara
├── estación
├── antena
├── ubicaciones
├── activación
├── observaciones
└── evidencias
```

## Conceptos Principales

### Centro

Identifica la carpeta de trabajo y la unidad principal de almacenamiento del certificado.

### Ubicación

Representa un sector físico dentro del centro.

Ejemplos:

- Pontón
- Jaula 101
- Jaula 105
- Jaula 106

Una ubicación puede contener varios equipos.

### Equipo

Representa un monitor físico instalado.

Características principales:

- Número correlativo único dentro del certificado.
- Asociación a una ubicación.
- Asociación a un sensor.

### Sensor

Representa el instrumento de medición instalado en un equipo.

Ejemplos:

- Oxígeno
- Salinidad
- Temperatura
- Corriente
- Turbidez
- pH

## Reglas Del Modelo

- La numeración de equipos es global para todo el certificado.
- El nombre visible de un equipo se deriva del número.
- Las ubicaciones pueden reutilizarse durante la construcción del certificado.
- `metadata` conserva trazabilidad técnica del archivo.
- `observaciones` queda como texto libre de cierre.

## Relación Con El Código

- `src/models/certificado.py` define la entidad contenedora principal.
- `src/models/ubicacion.py` agrupa equipos dentro de un sector.
- `src/models/equipo.py` referencia un sensor y un número de equipo.
- `src/models/sensor.py` describe la lectura asociada.
- `src/models/activacion.py` contiene las validaciones de soporte.
- `src/models/evidencia.py` representa archivos adjuntos.
- `src/models/metadata.py` guarda datos internos de control.
