# Documentación del Proyecto

Esta carpeta reúne la documentación funcional y técnica del generador de certificados de instalación.

## Orden sugerido de lectura

1. `modelo_datos.md` para entender qué representa el certificado.
2. `estructura_json.md` para ver la forma exacta del archivo guardado.
3. `flujo_operacional.md` para revisar el proceso de uso.
4. `tui.md` para conocer el menú y las pantallas disponibles.
5. `clases.md` para revisar las entidades del modelo.
6. `especificacion_campos.md` para consultar campos y reglas por sección.
7. `arquitectura.md` para una vista general de capas y responsabilidades.
8. `flujo_certificado.md` y `formato_certificado.md` para el ciclo de vida y el formato de salida.
9. `roadmap.md` para ver lo pendiente.

## Propósito de cada archivo

- `arquitectura.md`: visión general del diseño por capas.
- `clases.md`: referencia técnica de las clases y atributos del modelo.
- `especificacion_campos.md`: detalle de campos por sección.
- `estructura_json.md`: estructura persistida en `certificado.json`.
- `flujo_certificado.md`: recorrido del certificado desde creación hasta guardado.
- `flujo_operacional.md`: secuencia operativa del trabajo diario.
- `formato_certificado.md`: formato esperado para la salida documental.
- `modelo_datos.md`: explicación conceptual del dominio y sus relaciones.
- `roadmap.md`: funcionalidades pendientes y prioridades.
- `tui.md`: navegación actual de la interfaz de texto.

## Estado Actual

- La persistencia principal es un archivo `certificado.json` por centro y año.
- La TUI permite editar solo una parte del certificado hoy.
- Varias secciones del modelo existen en datos, pero aún no tienen pantalla completa en la interfaz.
- La generación de PDF y la gestión avanzada de evidencias deben tratarse como trabajo pendiente si no aparecen descritas en el código.
