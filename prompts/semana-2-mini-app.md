# Mini-aplicación de práctica: Trivia de cultura general

## Versión A

**Objetivo:** construir la mini-aplicación con un prompt de una línea.
**Herramienta y modelo:** GitHub Copilot con el modelo GPT-4o.
**Prompt:**
```text
Haz una app web de trivia con FastAPI.
```
**Resultado:** La aplicación arrancó en http://127.0.0.1:8000 con un diseño básico pero con endpoints y estructura arbitraria (`main.py` plano en la raíz, rutas `/preguntas` y `/verificar`). Pruebas de aceptación aprobadas: 0 de 6 (error de importación `ModuleNotFoundError: No module named 'app'`). Ruff reportó 3 errores de estilo e importaciones.

## Versión B

**Objetivo:** construir la misma aplicación con un prompt estructurado, AGENTS.md y pruebas de aceptación.
**Herramienta y modelo:** GitHub Copilot con el modelo GPT-4o.
**Prompt:**
```markdown
## Rol
Actúa como un desarrollador backend sénior en FastAPI con experiencia en código modular.

## Objetivo
Construir una aplicación web de trivia de cultura general con FastAPI y plantillas Jinja2, que cumpla estos requisitos:
1. GET / muestra una página que presenta las preguntas una por una, con cuatro botones de opción, indica si la respuesta fue correcta y muestra el puntaje acumulado.
2. GET /api/preguntas devuelve una lista de 5 preguntas de cultura general. Cada pregunta tiene los campos id (entero), texto (texto) y opciones (lista de 4 textos). La respuesta correcta no se incluye.
3. POST /api/responder recibe {"id": 1, "opcion": 2}, donde opcion es un índice de 0 a 3, y devuelve {"correcta": true o false, "respuesta_correcta": índice de 0 a 3}.
4. Si el id no existe, responde con el código 404. Si la opción no está entre 0 y 3, responde con el código 422.

## Contexto
Lee AGENTS.md y tests/test_aceptacion.py. La arquitectura debe ser modular: las rutas en app/main.py y la lógica de preguntas y validación en app/servicios.py.

## Restricciones
- No modifiques tests/test_aceptacion.py bajo ninguna circunstancia.
- No agregues librerías externas que no estén en requirements.txt.
- No escribas lógica de negocio directamente en las funciones de las rutas.

## Formato de salida
Antes de escribir código, muestra el plan con las rutas completas de los archivos y espera mi aprobación.

## Ejemplo
GET /api/preguntas devuelve:
[{"id": 1, "texto": "¿Cuál es el planeta más grande del sistema solar?", "opciones": ["Marte", "Júpiter", "Saturno", "Venus"]}]

POST /api/responder con {"id": 1, "opcion": 1} devuelve:
{"correcta": true, "respuesta_correcta": 1}

## Criterio de éxito
Las pruebas de aceptación en tests/test_aceptacion.py pasan al 100% con pytest -v y ruff check . pasa sin advertencias ni errores. Si después de 3 intentos no se cumple, detente y explica el problema.
```
**Resultado:** El modelo presentó un plan claro de 4 pasos con rutas modulares (`app/__init__.py`, `app/servicios.py`, `app/main.py`, `app/templates/index.html`). Tras la aprobación, generó el código sin tocar el contrato. Necesitó 1 solo intento de generación y un ajuste menor de tipado Ruff (`list[str]`). Pruebas de aceptación aprobadas: 6 de 6 (100%). Errores de Ruff: 0 checks failed.

## Mejora

**Objetivo:** Agregar parámetro de consulta `cantidad` opcional (1 a 5, por defecto 5) en `GET /api/preguntas`, validando con código 422 si está fuera de rango, y actualizar la interfaz con un selector interactivo.
**Herramienta y modelo:** GitHub Copilot con el modelo GPT-4o.
**Prompt:**
```markdown
## Rol
Actúa como desarrollador backend y frontend en FastAPI.

## Objetivo
Agregar a la mini-aplicación de trivia la siguiente mejora:
1. El endpoint GET /api/preguntas debe aceptar un parámetro de consulta opcional llamado cantidad, con valor entre 1 y 5 (por defecto 5).
2. Si el parámetro cantidad no está entre 1 y 5, debe responder con código HTTP 422.
3. La página principal (GET /) debe incluir un selector para que el usuario elija cuántas preguntas desea responder antes de iniciar la trivia.

## Contexto
Lee AGENTS.md, app/main.py, app/servicios.py, app/templates/index.html y tests/test_aceptacion.py.

## Restricciones
- No modifiques tests/test_aceptacion.py.
- Crea las nuevas pruebas en tests/test_mejora.py.
- Mantén la separación: lógica en servicios.py y endpoint en main.py.

## Formato de salida
Muestra el plan con los archivos a modificar y crear, y espera mi aprobación.

## Criterio de éxito
pytest -v pasa todas las pruebas existentes y las nuevas (9 de 9), y ruff check . pasa sin errores.
```
**Resultado:** Creó `tests/test_mejora.py` con 3 pruebas nuevas, actualizó `app/servicios.py` y `app/main.py` con `Query(5, ge=1, le=5)`, y agregó el selector en `app/templates/index.html`. Pruebas totales aprobadas: 9 de 9. Errores de Ruff: 0.

## Comparación

| Criterio | Versión A | Versión B |
| :--- | :--- | :--- |
| **Mensajes enviados** | 1 | 2 (Prompt estructurado + Aprobación del plan) |
| **¿Arranca la aplicación?** | Sí | Sí |
| **Requisitos del anexo cumplidos** | 1 de 4 (Solo GET / funcional) | 4 de 4 (100% de requisitos funcionales y de contrato) |
| **Pruebas de aceptación aprobadas** | 0 de 6 (0%) | 6 de 6 (100%) |
| **Errores de Ruff** | 3 errores | 0 errores |
| **Separación de capas** | No (código monolítico en `main.py`) | Sí (`app/main.py` para rutas, `app/servicios.py` para lógica) |
| **Decisiones arbitrarias del LLM** | 3 (rutas inventadas, estructura plana, sin validaciones) | 0 (siguió exactamente el contrato y las restricciones) |

### Conclusión
La diferencia entre la Versión A y la Versión B demuestra que la precisión y la arquitectura del software generado por un LLM dependen directamente de la calidad del contexto y las restricciones proporcionadas. 
1. **Calidad del código:** En la Versión A el modelo asumió nombres de endpoints y estructuras que rompieron la compatibilidad con las pruebas de aceptación. En la Versión B, al contar con un contrato explícito (`AGENTS.md` y `test_aceptacion.py`), el código se organizó limpiamente en capas y aprobó el 100% de las pruebas a la primera ejecución.
2. **Control arquitectónico:** Prohibir explícitamente modificar las pruebas y exigir un plan previo evitó alucinaciones y modificaciones del contrato.
3. **Mantenibilidad:** La estructura modular de la Versión B facilitó extender la funcionalidad en la Actividad 5 (agregar el parámetro de cantidad) en minutos y sin regresiones.
