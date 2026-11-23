# STATE.md

Estado del proyecto. Léalo al iniciar cada sesión de trabajo y actualícelo al cerrarla.

## Estado actual

Repositorio publicado en GitHub con el CI en verde.
Página de inicio, /salud, /docs y /api/version funcionando en https://plataforma-ludica-ee5t.onrender.com.

## Decisiones

| Fecha | Decisión | Motivo |
| --- | --- | --- |
| 2026-11-23 | Usar la plantilla del curso con FastAPI | Es el stack definido para el proyecto |
| 2026-11-23 | Agregar endpoint GET /api/version | Exponer la versión oficial definida en app/proyecto.py de forma programática |

## Siguiente paso

Implementar el modelo de datos SQLModel y el servicio de cálculo de la mecánica de Racha diaria en app/servicios con sus pruebas unitarias.
