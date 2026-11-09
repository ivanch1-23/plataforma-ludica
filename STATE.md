# STATE.md

Estado del proyecto. Léalo al iniciar cada sesión de trabajo y actualícelo al cerrarla.

## Estado actual

Plantilla creada, personalizada para Ivan Andres Diaz Lizcano (Inglés con Racha diaria) y desplegada en Render con integración continua en verde.
Especificación funcional, flujos de usuario, plan técnico y ADR definidos en `/specs`.

## Decisiones

| Fecha | Decisión | Motivo |
| --- | --- | --- |
| 2026-11-09 | Adopción de Racha Diaria calculada reactivamente en backend (ADR 0001) | Garantizar integridad de datos y permitir seguimiento al docente. |

## Siguiente paso

Implementar el modelo de datos SQLModel y el servicio de cálculo de racha diaria con sus pruebas unitarias.
