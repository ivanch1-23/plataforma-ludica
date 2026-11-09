# Entrega de la semana 1

## Qué decidí

Configuré el repositorio del proyecto con mis datos de autoría (Ivan Andres Diaz Lizcano), asignando el curso de Inglés con la mecánica de juego de Racha diaria según el Anexo A del taller.
Decidí usar Render con el Blueprint render.yaml para automatizar la integración continua y despliegue del servicio web FastAPI.
Para la mecánica de Racha diaria, definí que se incentivará la práctica diaria otorgando puntos extra progresivos que se reinician al día 1 si el niño falta a un día de práctica.

## Qué delegué a la IA y cómo la dirigí

Delegué a la IA la extracción del contenido del PDF del taller para entender los requerimientos específicos de la materia Inglés (B.4) y la mecánica Racha diaria (C.5).
Le pedí asistir en la corrección de errores de autenticación con Git y en la verificación de pruebas automatizadas y chequeo de estilo con Ruff.

## Cómo verifiqué

1. Ejecuté pytest en local obteniendo 6 pruebas aprobadas (6 passed).
2. Ejecuté ruff check . obteniendo All checks passed.
3. Verifiqué que la aplicación desplegada en Render responde con estado ok en /salud y entrega los datos del proyecto en /api/proyecto.
4. Verifiqué la documentación interactiva en /docs de la aplicación en Render.
