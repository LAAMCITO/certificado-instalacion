# Flujo Operacional

## Secuencia Actual

1. El usuario abre la TUI.
2. Crea un nuevo certificado indicando el centro.
3. Completa o ajusta los datos generales.
4. Registra la infraestructura principal.
5. Configura el acceso remoto.
6. Guarda el certificado en `storage/certificados/<año>/<centro>/certificado.json`.
7. Luego puede volver a abrir el mismo certificado para seguir editándolo.

## Pantallas Implementadas

- `Datos Generales`
- `Infraestructura`
- `Acceso Remoto`

## Pantallas Pendientes En La TUI

- Cámara
- Estación
- Antena
- Ubicaciones
- Activación
- Evidencias

## Reglas Operacionales

- El centro identifica la carpeta de almacenamiento.
- La numeración y el contenido del certificado se deben mantener consistentes entre aperturas.
- La información se guarda por año, lo que facilita listar certificados existentes.
- Las secciones no implementadas deben quedar documentadas como futuras extensiones, no como flujo activo.
