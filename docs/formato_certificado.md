# Formato Del Certificado

## Formato De Salida Actual

Hoy el certificado se guarda como archivo JSON estructurado. El formato base es:

```text
storage/certificados/<año>/<centro>/certificado.json
```

## Convenciones

- El nombre de la carpeta del centro coincide con el valor de `datos_generales.centro`.
- El año organiza la colección de certificados por período.
- El JSON usa sangría legible para facilitar revisión manual.
- Los textos se guardan en UTF-8.

## Formato Esperado Para Salida Documental

Si más adelante se genera un documento PDF, debería conservar:

- identificación del centro;
- datos generales;
- infraestructura;
- acceso remoto;
- resumen de ubicaciones y equipos;
- validación de activación;
- evidencias asociadas.

## Estado

- El formato JSON está confirmado por el servicio de persistencia.
- El formato PDF debe documentarse como objetivo futuro hasta que exista una implementación completa en el código.
