# Especificación: Plataforma Lúdica de Inglés con Racha Diaria

## Contexto

- **Cliente:** Un instituto de inglés para niños.
- **Público objetivo:** Colegios de primaria en los que el docente de aula dicta todas las materias y no domina el idioma inglés.
- **Problema que resuelve:** Permite que los niños de 6 a 10 años aprendan vocabulario de inglés (animales, colores, números, comida, familia, partes de la casa y objetos del salón) mediante actividades de preguntas con opciones, mientras el docente dispone de contenido precargado y consulta el avance sin necesitar conocimientos de inglés.
- **Mecánica lúdica (Racha diaria):** Incentiva la práctica diaria otorgando 10 puntos base por día jugado más 5 puntos extra por cada día consecutivo a partir del segundo (hasta un máximo de 25 puntos extra), reiniciando la racha a 1 si pasa un día calendario sin completar ninguna actividad.
- **Acceso:** Dos roles diferenciados: docente y niño. El niño ingresa sin correo ni contraseña usando el código de la clase, su alias y uno de los 6 avatares disponibles (`colibri`, `tortuga`, `delfin`, `jaguar`, `buho` y `rana`). Durante el curso solo se usan datos ficticios.

---

## Historias de usuario

### H1. El docente gestiona las actividades del curso

Como **docente**,
quiero **crear, consultar, actualizar y eliminar actividades con sus preguntas**,
para **mantener actualizado el contenido de vocabulario de inglés de mi curso**.

**Criterios de aceptación:**
- Dado que el docente envía una actividad con un título no vacío, un orden numérico y al menos 5 preguntas (cada una con 3 o 4 opciones y una respuesta correcta incluida entre esas opciones), cuando la guarda, entonces el sistema la registra y responde con el identificador asignado a la actividad y a cada pregunta.
- Dado que el docente intenta guardar una actividad con título vacío, con menos de 5 preguntas, con una pregunta de menos de 3 o más de 4 opciones, o con una respuesta correcta fuera de las opciones, cuando la envía, entonces el sistema rechaza la operación con un error de validación (código 422).
- Dado que existen actividades registradas, cuando el docente consulta la lista, las actualiza o elimina una actividad existente, entonces la lista se devuelve ordenada por el campo `orden`, la actualización reemplaza sus datos y preguntas, y la eliminación borra tanto la actividad como sus preguntas asociadas.

### H2. La plataforma inicia con contenido del curso

Como **docente**,
quiero **que la plataforma cargue automáticamente una clase de ejemplo, niños ficticios y actividades de inglés al iniciar por primera vez**,
para **empezar a usar el curso sin tener que crear el contenido desde cero**.

**Criterios de aceptación:**
- Dado que la base de datos está vacía (sin ninguna clase registrada), cuando la aplicación inicia, entonces carga exactamente 1 clase con un código de 6 caracteres, 3 niños ficticios con alias y avatar de la lista permitida, y 3 actividades de inglés con 5 preguntas cada una (3 o 4 opciones y 1 respuesta correcta por pregunta).
- Dado que la base de datos ya contiene al menos una clase registrada, cuando la aplicación inicia nuevamente, entonces no inserta registros nuevos ni duplica la clase, los niños ni las actividades existentes.

### H3. El niño entra con el código de la clase, su alias y un avatar

Como **niño**,
quiero **entrar a la plataforma escribiendo el código de mi clase, eligiendo mi alias y seleccionando un avatar**,
para **ingresar a mis actividades de inglés sin usar correo electrónico ni contraseña**.

**Criterios de aceptación:**
- Dado un código de clase válido de 6 caracteres, cuando el niño lo escribe, entonces el sistema muestra la lista de alias de los niños registrados en esa clase y los 6 avatares disponibles (`colibri`, `tortuga`, `delfin`, `jaguar`, `buho` y `rana`).
- Dado que el niño selecciona su alias de la lista de la clase y uno de los 6 avatares permitidos, cuando confirma el ingreso, entonces accede a su sesión de juego sin que se le solicite correo ni contraseña.
- Dado un código de clase que no existe en la base de datos, cuando el niño intenta ingresar con ese código, entonces el sistema rechaza el ingreso e informa que el código no corresponde a ninguna clase.

### H4. El niño resuelve una actividad y sabe de inmediato si acertó

Como **niño**,
quiero **responder las preguntas de una actividad de vocabulario y recibir confirmación inmediata en cada respuesta**,
para **saber al instante si acerté o cuál era la palabra correcta en inglés**.

**Criterios de aceptación:**
- Dado que el niño inicia una actividad de al menos 5 preguntas, cuando responde una pregunta seleccionando una de las 3 o 4 opciones, entonces el sistema le indica de inmediato si la opción elegida coincide o no con la respuesta correcta.
- Dado que el niño responde todas las preguntas de la actividad, cuando finaliza la última pregunta, entonces el sistema registra un intento con la cantidad de aciertos, el total de preguntas, la duración en segundos, la fecha y el porcentaje de aciertos calculado como `(aciertos / total) * 100`.

### H5. La plataforma aplica la regla de la mecánica

Como **niño**,
quiero **acumular puntos diarios y aumentar mi racha al completar actividades en días seguidos**,
para **mantener mi constancia diaria practicando vocabulario en inglés**.

**Criterios de aceptación:**
- Dado que el niño completa su primera actividad en la fecha actual de Colombia y es su primer día de racha (o pasó al menos un día calendario sin completar actividades), cuando termina la actividad, entonces su racha actual queda en 1 día y suma 10 puntos base (0 puntos extra).
- Dado que el niño completó al menos una actividad el día anterior (según la fecha de Colombia), cuando completa una actividad hoy por primera vez en el día, entonces su racha actual aumenta en 1 y recibe 10 puntos base más 5 puntos extra por cada día de racha a partir del segundo, con un tope de 25 puntos extra (15 puntos en el día 2, 20 en el día 3 y 35 del día 6 en adelante).
- Dado que el niño ya completó una actividad hoy (fecha de Colombia), cuando termina otra actividad el mismo día, entonces la racha actual no aumenta ni se suman más puntos diarios, y se conserva actualizada la racha más larga si la racha actual la supera.

### H6. El docente consulta el progreso de cada niño

Como **docente**,
quiero **ver las métricas de práctica, las actividades completadas, la racha actual, la racha más larga y los puntos de cada niño de mi clase**,
para **hacer seguimiento del avance individual de mis estudiantes**.

**Criterios de aceptación:**
- Dado un niño que ha registrado uno o más intentos en la plataforma, cuando el docente consulta el progreso de la clase, entonces visualiza por cada niño la suma total de la duración en segundos de sus intentos como tiempo de juego y el conteo de actividades distintas completadas sin repetir.
- Dado un niño con historial de juego en la mecánica Racha diaria, cuando el docente consulta su progreso, entonces visualiza su racha actual, su racha más larga registrada y el total de puntos acumulados.

---

## Requisitos funcionales

| Código | Requisito | Historia |
| --- | --- | --- |
| **RF1** | Gestionar actividades (listar en orden, crear, consultar por id, actualizar reemplazando preguntas y eliminar en cascada) validando título, mínimo 5 preguntas, 3 o 4 opciones y respuesta correcta válida. | H1 |
| **RF2** | Ejecutar carga inicial idempotente de 1 clase (código de 6 caracteres), 3 niños ficticios y 3 actividades de 5 preguntas de inglés cuando no existan clases. | H2 |
| **RF3** | Permitir el ingreso del niño mediante código de clase de 6 caracteres, selección de alias de esa clase y selección de uno de los 6 avatares permitidos. | H3 |
| **RF4** | Presentar actividades de preguntas con 3 o 4 opciones, dar retroalimentación inmediata por pregunta y guardar el intento completo con aciertos, total, duración en segundos y fecha. | H4 |
| **RF5** | Calcular y actualizar la racha actual, la racha más larga y los puntos diarios según la fecha calendario de Colombia (10 base + 5 extra desde el día 2 hasta máximo 25 extra; 1 intento puntuable por día; reinicio a 1 tras un día sin jugar). | H5 |
| **RF6** | Mostrar al docente por cada niño el tiempo total de juego, las actividades completadas sin repetir, la racha actual, la racha más larga y los puntos acumulados. | H6 |

---

## Requisitos no funcionales

| Código | Requisito | Cómo se verifica |
| --- | --- | --- |
| **RNF1** | Arquitectura en capas desacopladas (`app/rutas/`, `app/servicios/`, `app/modelos/`). | Revisión de código y ausencia de lógica de negocio en las rutas. |
| **RNF2** | Privacidad de menores: no solicitar nombres completos reales, correos ni contraseñas; usar únicamente alias ficticios. | Revisión de los modelos de datos, carga inicial y formularios de ingreso. |
| **RNF3** | Validación estricta de entrada mediante esquemas de Pydantic y respuestas HTTP estándar (200, 201, 204, 404, 422). | Pruebas automatizadas en `tests/aceptacion/`. |
| **RNF4** | Calidad de código y cobertura de pruebas automatizadas sobre rutas, servicios y carga inicial. | Ejecución de `pytest -v` y `ruff check .` sin errores. |

---

## Casos límite

1. **Múltiples actividades el mismo día:** Si el niño completa 2 o más actividades en la misma fecha de Colombia, se registran todos los intentos para sus métricas de tiempo y actividades completadas, pero la racha y los puntos diarios solo se otorgan una vez al día.
2. **Reinicio por inactividad:** Si el último día jugado fue hace 2 días o más (al menos un día calendario completo sin completar una actividad), la racha actual se reinicia a 1 y ese día otorga 10 puntos.
3. **Repetición de una misma actividad:** Si el niño completa la misma actividad varias veces, las métricas del docente suman la duración de todos los intentos, pero cuentan esa actividad una sola vez dentro de las actividades completadas.
4. **Carga inicial repetida:** Ejecutar la función de carga inicial múltiples veces sobre la misma base de datos mantiene exactamente 1 clase, 3 niños y 3 actividades iniciales.

---

## Fuera de alcance

- Actividades interactivas distintas a preguntas de selección con 3 o 4 opciones y una respuesta correcta (por ejemplo, arrastrar objetos del salón hasta su nombre en inglés o tocar un color en pantalla tras escuchar un audio).
- Evaluación o procesamiento de pronunciación mediante micrófono con reconocimiento de voz (el encargo menciona idealmente pronunciar bien, lo cual queda fuera del alcance del MVP).
- Gestión de múltiples cursos o creación de cuentas de docente con correo y contraseña, pagos o suscripciones en línea y chat entre estudiantes.

---

## Dudas abiertas

| N.º | Duda | Tipo | Supuesto | Justificación |
| --- | --- | --- | --- | --- |
| 1 | ¿Qué define con exactitud que un niño «aprendió» una palabra? | Ambigüedad | Se considera aprendida si el niño acierta la pregunta asociada en 3 actividades consecutivas sin cometer errores. | Establece un criterio objetivo, verificable mediante pruebas automatizadas y claro para el docente. |
| 2 | ¿Cómo evalúa el sistema si el niño «pronuncia bien» la palabra en la web? | Vacío | En el MVP no hay evaluación fonética por micrófono; este aspecto queda fuera de alcance y se prioriza el reconocimiento escrito en preguntas con opciones. | El reconocimiento de voz en navegadores escolares con baja conectividad introduce alta latencia y fallos de permisos. |
| 5 | ¿Al reiniciarse la racha a 1 día se pierden los puntos acumulados por el niño? | Ambigüedad | No; los puntos acumulados se conservan permanentemente y solo se reinicia el contador de días seguidos a 1. | Penalizar quitando puntos desmotiva a los estudiantes y genera rechazo a la plataforma. |
| 7 | El encargo afirma «que el docente no tenga que preparar nada» pero también que «elige los temas». ¿Cómo se concilian? | Contradicción | El sistema incluye actividades precargadas al iniciar y el docente puede gestionar o ajustar las actividades disponibles según su clase. | Cumple con cero preparación inicial al tiempo que permite al docente personalizar el contenido. |
| 9 | El cliente indica que muchos colegios tienen conexión lenta, pero se requieren recursos livianos. ¿Cómo se garantiza la fluidez? | Ambigüedad | Los recursos estáticos y de PWA se mantienen ligeros y cacheados mediante el Service Worker incluido en la aplicación. | Permite que la aplicación cargue rápidamente aun con intermitencia de red escolar. |
| 10 | ¿Cómo se mide el «tiempo que practica» cada niño si deja la pantalla abierta? | Vacío | La duración de cada intento se registra en segundos al completar la actividad y se sugiere pausar el temporizador del cliente tras 60 segundos sin interacción. | Previene datos distorsionados si el estudiante deja el navegador abierto sin responder. |
