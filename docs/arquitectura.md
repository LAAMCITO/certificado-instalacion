# Arquitectura

## Visión General

El proyecto sigue una arquitectura simple por capas:

- Interfaz de texto en `src/tui`.
- Lógica de persistencia en `src/services`.
- Modelo de datos en `src/models`.
- Almacenamiento local en `storage/certificados/<año>/<centro>/certificado.json`.

## Flujo De Datos

```text
Usuario
  -> TUI
  -> certificado en memoria
  -> servicio de guardado
  -> JSON en almacenamiento local
```

## Responsabilidades

- `src/tui`: muestra menús, solicita datos y edita secciones del certificado.
- `src/services/certificado_service.py`: crea el certificado, lo guarda y lo carga.
- `src/models`: define la estructura base del certificado y sus entidades auxiliares.
- `storage/`: conserva los certificados generados por año y centro.

## Alcance Actual

- La aplicación está orientada a uso interno.
- La persistencia existente es local y basada en archivos.
- La interfaz muestra secciones que todavía no están completas.
- La salida PDF debe considerarse pendiente hasta que el flujo quede confirmado por el código.

## Dependencias De Diseño

- El certificado se maneja en memoria como un diccionario anidado una vez cargado desde JSON.
- Parte del modelo está fuertemente tipada con `dataclass` y parte queda como `dict`.
- El almacenamiento usa la carpeta del centro como unidad principal de organización.
