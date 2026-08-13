# Especificación De Campos

## Datos Generales

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| Responsable | `responsable` | Sí | Persona de soporte que registra el certificado. |
| Empresa | `empresa` | Sí | Empresa asociada al centro. |
| Centro | `centro` | Sí | Identificador de la carpeta del certificado. |
| Fecha de instalación | `fecha_instalacion` | Sí | Fecha del trabajo en terreno. |
| Técnico visita | `tecnico_visita` | Sí | Nombre del técnico que realizó la instalación. |
| Número ficha | `numero_ficha` | Sí | Número de respaldo o documento del terreno. |

## Infraestructura

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| Categoría | `categoria` | Sí | Tipo de equipo principal. |
| Marca | `marca` | Sí | Marca del equipo. |
| Modelo | `modelo` | Sí | Modelo del equipo. |
| Serie | `serie` | Sí | Número de serie del equipo. |
| Sistema operativo | `sistema_operativo` | Sí | SO utilizado por el equipo. |
| Conectividad | `conectividad` | Sí | Tipo de conexión del sistema. |
| Switch | `switch` | No | Solo aplica a conectividad cableada. |
| Puerto | `puerto` | No | Solo aplica a conectividad cableada. |

## Acceso Remoto

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| Protocolo | `protocolo` | Sí | Define el esquema de acceso. |
| Tun0 | `tun0` | No | Se usa cuando el protocolo lo requiere. |
| IP Fija | `ip_fija` | No | Se usa cuando el protocolo lo requiere. |
| Puerto servidor | `puerto_server` | Sí | Puerto usado para acceso remoto. |

## Cámara

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| Instalada | `instalada` | Sí | Marca si existe cámara. |
| Tipo IP | `tipo_ip` | No | Aplica si la cámara está instalada. |
| Dirección IP | `direccion_ip` | No | Aplica si la cámara está instalada. |

## Estación

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| Instalada | `instalada` | Sí | Marca si existe estación. |
| Tipo | `tipo` | No | Describe el tipo de estación. |

## Antena

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| Versión | `version` | No | Campo esperado por documentación histórica. |
| Tipo antena | `tipo_antena` | No | Describe el modelo o tipo físico. |
| PAN ID | `pan_id` | No | Identificador de red. |
| Ubicación física | `ubicacion_fisica` | No | Ubicación de instalación. |
| Observación | `observacion` | No | Texto libre. |

## Ubicaciones

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| Tipo | `tipo` | Sí | Nombre del sector o referencia. |
| Nombre | `nombre` | Sí | Identificador visible. |
| Coordenadas | `coordenadas` | No | Posición física del sector. |
| Equipos | `equipos` | No | Lista de equipos dentro de la ubicación. |

## Equipo

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| Número de equipo | `numero_equipo` | Sí | Correlativo global dentro del certificado. |
| MAC | `mac` | No | Identificador físico del equipo. |
| Sensor | `sensor` | No | Objeto asociado al equipo. |

## Sensor

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| Tipo | `tipo` | Sí | Tipo de medición. |
| Profundidad | `profundidad` | No | Profundidad de lectura. |
| Serial | `serial` | No | Número de serie del sensor. |

## Activación

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| Fecha creación monitor | `fecha_creacion_monitor` | Sí | Fecha de creación o activación del monitor. |
| Tipo IP | `tipo_ip` | Sí | Tipo de IP validada. |
| IP final | `ip_final` | No | IP usada como resultado final. |
| Ping OK | `ping_ok` | Sí | Validación de conectividad. |
| SSH OK | `ssh_ok` | Sí | Validación de acceso. |
| Datos visibles | `datos_visibles` | Sí | Confirmación de información en plataforma. |
| Transmisión OK | `transmision_ok` | Sí | Confirmación de transmisión. |
| Alarmas activadas | `alarmas_activadas` | Sí | Confirmación de alertas. |
| Responsable activación | `responsable_activacion` | Sí | Persona que valida la activación. |
| Estado final | `estado_final` | Sí | Resultado del proceso. |

## Evidencias

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| Archivo | `archivo` | Sí | Nombre del archivo adjunto. |
| Ruta | `ruta` | Sí | Ubicación relativa o absoluta. |

## Metadata

| Campo | Clave | Obligatorio | Observación |
| --- | --- | --- | --- |
| UUID | `uuid` | Sí | Identificador único del certificado. |
| Versión modelo | `version_modelo` | Sí | Versión del esquema usado. |
| Fecha creación | `fecha_creacion` | Sí | Fecha de generación inicial. |
| Fecha modificación | `fecha_modificacion` | Sí | Última actualización del archivo. |
