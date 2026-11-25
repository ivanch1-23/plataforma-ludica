# STATE.md

Estado del proyecto. Léalo al iniciar cada sesión de trabajo y actualícelo al cerrarla.

## Estado actual

Especificación del MVP (`specs/spec.md` y `specs/respuestas-cliente.md`), modelo de datos SQLModel (`app/modelos/__init__.py`, `app/db.py`, diagrama ER en `specs/plan.md`), API CRUD de actividades (`/api/actividades`) y carga inicial idempotente del curso de Inglés (`app/datos_iniciales.py`) terminados en la rama `taller-8/actividades`.
Las 21 pruebas (`tests/test_inicio.py`, `tests/aceptacion/test_actividades.py` y `tests/aceptacion/test_datos_iniciales.py`) y `ruff check .` pasan sin errores. Pendiente commit/push, pull request en GitHub, verificación en Render y etiqueta `taller-8`.

## Decisiones

| Fecha | Decisión | Motivo |
| --- | --- | --- |
| 2026-11-23 | Usar la plantilla del curso con FastAPI | Es el stack definido para el proyecto |
| 2026-11-23 | Agregar endpoint GET /api/version | Exponer la versión oficial definida en app/proyecto.py de forma programática |
| 2026-11-25 | Adoptar las reglas exactas de `specs/respuestas-cliente.md` (Racha diaria) en `specs/spec.md` | Prevalecen sobre los supuestos previos de `specs/dudas-encargo.md` y fijan criterios verificables |
| 2026-11-25 | Separar validaciones de entrada/salida en `app/esquemas.py` y lógica CRUD en `app/servicios/actividades.py` | Mantiene las rutas libres de lógica de negocio y garantiza respuestas 422 automáticas con Pydantic |
| 2026-11-25 | Guardar `opciones` en columna JSON y eliminar preguntas desde el servicio en `PUT` y `DELETE` | Permite almacenar listas en SQLite/PostgreSQL y asegura consistencia sin depender de cascadas SQL |
| 2026-11-25 | Verificar si existe al menos una `Clase` antes de insertar en `cargar_datos_iniciales` | Hace la carga inicial idempotente ante reinicios y redespliegues en Render |

## Siguiente paso

Taller 9: implementar la entrada del niño (código de clase, alias y avatar), la pantalla de juego con retroalimentación inmediata, el registro de intentos y el cálculo de la mecánica de Racha diaria junto con el progreso del docente.
