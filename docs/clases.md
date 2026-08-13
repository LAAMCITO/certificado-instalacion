# Clases Del Sistema

## Objetivo

Definir las entidades principales utilizadas por la aplicación de certificados de instalación.

Estas clases representan el modelo de datos que luego consume la TUI, el almacenamiento JSON y futuras salidas documentales.

## Certificado

Entidad principal del sistema.

Representa una instalación completa realizada en un centro.

### Atributos

- `metadata`
- `datos_generales`
- `infraestructura`
- `acceso_remoto`
- `camara`
- `estacion`
- `antena`
- `ubicaciones`
- `activacion`
- `observaciones`
- `evidencias`

## Ubicacion

Representa un sector físico dentro del centro.

### Atributos

- `tipo`
- `nombre`
- `coordenadas`
- `equipos`

## Equipo

Representa un monitor físico instalado.

### Reglas

- El número de equipo es correlativo y global dentro del certificado.
- El nombre visible del equipo se deriva del número.

### Atributos

- `numero_equipo`
- `mac`
- `sensor`

## Sensor

Representa el sensor instalado en un equipo.

### Atributos

- `tipo`
- `profundidad`
- `serial`

## Activacion

Representa la validación realizada por soporte.

### Atributos

- `fecha_creacion_monitor`
- `tipo_ip`
- `ip_final`
- `ping_ok`
- `ssh_ok`
- `datos_visibles`
- `transmision_ok`
- `alarmas_activadas`
- `responsable_activacion`
- `estado_final`

## Evidencia

Representa una referencia a una fotografía asociada al certificado.

### Atributos

- `archivo`
- `ruta`

## Metadata

Información técnica interna del certificado.

### Atributos

- `uuid`
- `version_modelo`
- `fecha_creacion`
- `fecha_modificacion`

## Nota De Implementación

- `camara`, `estacion` y `antena` se manejan actualmente como estructuras flexibles dentro de `Certificado`.
- `Ubicacion`, `Equipo`, `Sensor`, `Activacion`, `Evidencia` y `Metadata` están modeladas como `dataclass`.
