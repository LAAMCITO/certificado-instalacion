# Flujo Del Certificado

## Ciclo De Vida

1. Crear certificado desde la TUI.
2. Inicializar `metadata` y secciones base.
3. Completar datos generales, infraestructura y acceso remoto.
4. Abrir el certificado nuevamente si hace falta continuar la edición.
5. Guardar en `storage/certificados/<año>/<centro>/certificado.json`.
6. Mantener las evidencias junto al certificado.
7. Dejar listo el archivo para futuras salidas documentales.

## Estados Relevantes

- `nuevo`: el certificado fue creado pero aún está incompleto.
- `en edición`: el usuario sigue ajustando secciones.
- `guardado`: existe un JSON persistido en disco.
- `pendiente`: hay secciones del modelo que todavía no cuentan con interfaz completa.

## Puntos De Control

- `centro` define la ruta de persistencia.
- `metadata.uuid` identifica de forma única el archivo.
- `metadata.fecha_modificacion` debe reflejar la última edición.
- El contenido guardado debe permanecer compatible con cargas posteriores.
