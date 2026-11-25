# Respuestas del cliente: Racha diaria

Estas respuestas son obligatorias y prevalecen sobre los supuestos de specs/dudas-encargo.md.

## Para todas las mecánicas

- **Actividad:** grupo de preguntas del curso, con un mínimo de 5. Cada pregunta tiene un enunciado, de 3 a 4 opciones y una sola respuesta correcta.
- **Intento:** registro que se crea cuando un niño termina una actividad completa. Guarda los aciertos, el total de preguntas, la duración en segundos y la fecha.
- **Porcentaje de aciertos:** aciertos dividido por el total de preguntas, multiplicado por 100.
- **Contenido inicial:** al iniciar, la aplicación carga una clase de ejemplo, 3 actividades de 5 preguntas del curso y 3 niños ficticios, solo si la base de datos está vacía.
- **Entrada del niño:** el niño escribe el código de la clase, elige su alias en la lista de niños de esa clase y elige uno de los 6 avatares.
- **Métricas del docente:** el tiempo de juego es la suma de la duración de los intentos; las actividades completadas se cuentan sin repetir.

## Avatares

Los 6 avatares se identifican con estos valores, que se guardan en el campo avatar: colibri, tortuga, delfin, jaguar, buho y rana.

## Regla de la mecánica Racha diaria

- Un día cuenta para la racha si el niño termina al menos una actividad. Se usa la fecha de Colombia.
- Cada día jugado da 10 puntos base, más 5 puntos extra por cada día de racha a partir del segundo, con un máximo de 25 puntos extra. El día 1 da 10 puntos; el día 2, 15; el día 3, 20; del día 6 en adelante, 35.
- Jugar varias veces el mismo día no aumenta la racha ni suma más puntos.
- Si pasa un día sin jugar, la racha vuelve a 1.
- Se guardan la racha actual y la racha más larga de cada niño.
