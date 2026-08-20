# TUI - Certificado De Instalación

## Menú Principal

La aplicación muestra un menú simple de consola para crear o abrir certificados.

Opciones actuales:

- `1. Nuevo certificado`
- `2. Abrir certificado`
- `3. Salir`

## Crear Certificado

Al crear un certificado, el usuario ingresa el nombre del centro.
Luego el sistema:

- genera `metadata` con UUID y fechas;
- prepara las secciones base del certificado;
- guarda el JSON en `storage/certificados/<año>/<centro>/certificado.json`.

## Menú Del Certificado

Al abrir un certificado, la interfaz muestra:

- `1. Datos Generales`
- `2. Infraestructura`
- `3. Acceso Remoto`
- `4. Cámara`
- `5. Estación`
- `6. Antena`
- `7. Ubicaciones`
- `8. Activación`
- `9. Evidencias`
- `G. Guardar`
- `V. Volver`

## Pantallas Implementadas

### Datos Generales

- Muestra responsable, empresa, centro, fecha de instalación, técnico y número de ficha.
- Permite editar todos los campos salvo `centro`, que queda fijo.

### Infraestructura

- Permite definir la categoría del equipo principal.
- Registra marca, modelo, serie y sistema operativo.
- Ajusta conectividad, switch y puerto cuando corresponde.

### Acceso Remoto

- Permite definir el protocolo de acceso.
- Maneja `tun0`, `IP fija` y `puerto_server`.
- Limpia campos no aplicables cuando cambia el protocolo.

## Pantallas Pendientes

Estas opciones aparecen en el menú, pero todavía no tienen una pantalla completa implementada:

- Cámara
- Estación
- Antena
- Ubicaciones
- Activación
- Evidencias

## Comportamiento Actual

- La edición se realiza sobre un diccionario en memoria.
- El menú aún no confirma un flujo completo de guardado al salir de cada sección.
- El estado guardado depende del servicio de persistencia y del archivo JSON del certificado.
