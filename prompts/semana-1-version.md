# Registro de Prompt - Semana 1: Endpoint de Versión

## Objetivo
Agregar el endpoint GET /api/version que devuelva la versión oficial del proyecto con su respectiva prueba automatizada.

## Herramienta y modelo
Copilot, modelo Auto.

## Prompt
Lee AGENTS.md. Agrega el endpoint GET /api/version, que devuelva la versión definida en app/proyecto.py, con su prueba en tests/test_inicio.py. Antes de escribir código, explícame qué archivos vas a modificar y espera mi aprobación.

## Resultado
El agente propuso modificar exclusivamente app/rutas/api.py y tests/test_inicio.py. Se agregaron la ruta y el modelo Pydantic Version, y la prueba test_api_version_devuelve_la_version_del_proyecto. Las 7 pruebas pasaron exitosamente y Ruff no reportó errores.
