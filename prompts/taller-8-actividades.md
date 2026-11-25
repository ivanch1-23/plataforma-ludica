# Taller 8: especificación, modelo de datos y actividades

Curso: Inglés. Mecánica: Racha diaria.

## Especificación

**Objetivo:** redactar `specs/spec.md` con las seis historias del MVP y copiar `specs/respuestas-cliente.md` de Racha diaria.

**Herramienta y modelo:** Antigravity con Gemini 4 Hydrogen (High).

**Prompt:**

```markdown
## Rol
Actúa como analista de requisitos de software.

## Objetivo
Redactar en specs/spec.md la especificación del MVP de la plataforma, con la estructura que ya tiene ese archivo.

## Contexto
Lee AGENTS.md, specs/encargo.md, specs/ficha-mecanica.md, specs/dudas-encargo.md y specs/respuestas-cliente.md. Cuando una respuesta del cliente contradiga un supuesto de dudas-encargo.md, prevalece la respuesta del cliente.

## Restricciones
- Incluye exactamente estas seis historias de usuario:
  H1. El docente gestiona las actividades del curso.
  H2. La plataforma inicia con contenido del curso.
  H3. El niño entra con el código de la clase, su alias y un avatar.
  H4. El niño resuelve una actividad y sabe de inmediato si acertó.
  H5. La plataforma aplica la regla de la mecánica.
  H6. El docente consulta el progreso de cada niño.
- Cada historia tiene al menos dos criterios Dado/Cuando/Entonces, con los valores exactos de specs/respuestas-cliente.md.
- Todas las actividades son preguntas con 3 o 4 opciones y una respuesta correcta. Los demás tipos de actividad del encargo van en la sección Fuera de alcance.
- Las dudas que no responde el cliente van en Dudas abiertas, con el supuesto de dudas-encargo.md.
- No agregues funcionalidades que no estén en los documentos.
- En la tabla de Dudas abiertas, la columna Respuesta del cliente se renombra como Supuesto, porque esas dudas no tienen respuesta del cliente.
- Modifica solo specs/spec.md.

## Formato de salida
Antes de escribir, muestra la lista de historias con sus criterios resumidos en una línea cada uno y espera mi aprobación.

## Ejemplo
H5. Como niño, quiero acumular puntos diarios y aumentar mi racha al completar actividades en días seguidos, para mantener mi constancia diaria practicando vocabulario en inglés.
- Dado que el niño completó al menos una actividad el día anterior según la fecha de Colombia, cuando completa una actividad hoy por primera vez en el día, entonces su racha actual aumenta en 1 y suma 10 puntos base más 5 puntos extra por cada día de racha a partir del segundo, hasta un máximo de 25 puntos extra.
- Dado que el niño ya completó una actividad hoy, cuando termina otra actividad el mismo día, entonces la racha no aumenta ni se suman más puntos diarios.

## Criterio de éxito
Las seis historias tienen al menos dos criterios cada una y ningún criterio usa términos vagos como rápido, fácil o adecuado.
```

**Resultado:** Se incorporó `specs/respuestas-cliente.md` para Racha diaria y se redactó `specs/spec.md` con las 6 historias H1-H6, sus criterios verificables Dado/Cuando/Entonces con valores exactos (10 puntos base, +5 puntos extra por día desde el segundo con tope de 25, 6 avatares permitidos, mínimo 5 preguntas y 3-4 opciones), la sección Fuera de alcance y la tabla Dudas abiertas con la columna Supuesto. No requirió correcciones posteriores.

## Modelo de datos

**Objetivo:** crear los modelos SQLModel, `app/db.py`, el ciclo de vida en `app/main.py` y el diagrama entidad-relación en `specs/plan.md`.

**Herramienta y modelo:** Antigravity con Gemini 4 Hydrogen (High).

**Prompt:**

```markdown
## Rol
Actúa como desarrollador backend con experiencia en FastAPI y SQLModel.

## Objetivo
Crear el modelo de datos del MVP y la conexión con la base de datos:
1. En app/modelos/__init__.py, los modelos de tabla Clase, Nino, Actividad, Pregunta e Intento, con los campos del contrato.
2. En app/db.py, la variable motor, la función crear_tablas() y la dependencia obtener_sesion(), que entrega una sesión por petición.
3. En app/main.py, un ciclo de vida (lifespan) que llame a crear_tablas() al iniciar la aplicación.
4. En specs/plan.md, el diagrama entidad-relación en Mermaid, dentro de la sección Modelo de datos.

## Contexto
Lee AGENTS.md, specs/spec.md, specs/plan.md y app/main.py.
Contrato de datos:
- Clase: id, nombre, codigo (texto de 6 caracteres, único).
- Nino: id, alias, avatar, clase_id (clave foránea a Clase).
- Actividad: id, titulo, descripcion (texto opcional, vacío por defecto), orden (entero).
- Pregunta: id, enunciado, opciones (lista de textos), respuesta_correcta, actividad_id (clave foránea a Actividad).
- Intento: id, nino_id, actividad_id, aciertos, total, duracion_segundos, fecha (fecha y hora).

## Restricciones
- Usa exactamente los nombres de clases y campos del contrato.
- Guarda opciones en una columna JSON.
- La URL de la base de datos se lee de la variable de entorno DATABASE_URL, con el valor por defecto sqlite:///./plataforma.db.
- No agregues dependencias: sqlmodel ya está en requirements.txt.
- No crees endpoints ni modifiques las pruebas.

## Formato de salida
Antes de escribir código, muestra el plan con las rutas completas de los archivos y espera mi aprobación.

## Ejemplo
Pregunta(enunciado="¿Cómo se dice «perro» en inglés?", opciones=["Dog", "Cat", "Bird"], respuesta_correcta="Dog", actividad_id=1)

## Criterio de éxito
python -m pytest -v pasa todas las pruebas existentes, ruff check . no reporta errores y el comando python -c "import app.main" termina sin errores. No dejes ningún servidor en ejecución. Si después de 3 intentos no se cumple, detente y explica el problema.
```

**Resultado:** Se implementaron los 5 modelos de tabla en `app/modelos/__init__.py` (con `opciones` en columna JSON), el motor y sesión en `app/db.py`, el `lifespan` en `app/main.py` y el diagrama `erDiagram` en `specs/plan.md`. Las 7 pruebas existentes y `ruff check .` pasaron en el primer intento.

## API de actividades

**Objetivo:** implementar el CRUD de actividades (`/api/actividades`) hasta pasar todas las pruebas de aceptación.

**Herramienta y modelo:** Antigravity con Gemini 4 Hydrogen (High).

**Prompt:**

```markdown
## Rol
Actúa como desarrollador backend con experiencia en FastAPI y SQLModel.

## Objetivo
Implementar la API de actividades de la historia H1: crear, listar, consultar, actualizar y eliminar actividades con sus preguntas, según el contrato.

## Contexto
Lee AGENTS.md, la historia H1 de specs/spec.md, app/modelos/__init__.py, app/db.py, tests/aceptacion/conftest.py y tests/aceptacion/test_actividades.py. Las pruebas son el contrato: si el código y la prueba no coinciden, se corrige el código.
Contrato de la API:
- GET /api/actividades: 200 con la lista de actividades ordenadas por orden, cada una con sus preguntas.
- POST /api/actividades: 201 con la actividad creada, su id y el id de cada pregunta.
- GET /api/actividades/{id}: 200, o 404 si no existe.
- PUT /api/actividades/{id}: 200 y reemplaza titulo, descripcion, orden y preguntas, o 404 si no existe.
- DELETE /api/actividades/{id}: 204 y elimina también sus preguntas, o 404 si no existe.
- Responde 422 si el titulo está vacío, si hay menos de 5 preguntas, si una pregunta tiene menos de 3 o más de 4 opciones, o si la respuesta correcta no está entre las opciones.

## Restricciones
- La lógica va en app/servicios/actividades.py y las rutas en app/rutas/actividades.py, sin lógica de negocio. El router se registra en app/main.py.
- Las validaciones se declaran en esquemas de Pydantic para que FastAPI responda 422.
- El router usa tags=["Actividades"], para que /docs agrupe las operaciones en la sección Actividades.
- La sesión se recibe con Annotated[Session, Depends(obtener_sesion)], porque Ruff rechaza Depends como valor por defecto (regla B008).
- No modifiques ningún archivo de la carpeta tests.
- No agregues dependencias.

## Formato de salida
Antes de escribir código, muestra el plan con las rutas completas de los archivos y espera mi aprobación.

## Ejemplo
POST /api/actividades con {"titulo": "Animales en inglés", "orden": 1, "preguntas": [{"enunciado": "¿Cómo se dice «perro» en inglés?", "opciones": ["Dog", "Cat", "Bird"], "respuesta_correcta": "Dog"}, y cuatro preguntas más]} responde 201 con la misma actividad, su id y el id de cada pregunta.

## Criterio de éxito
python -m pytest -v pasa todas las pruebas, incluidas las de tests/aceptacion/test_actividades.py, y ruff check . no reporta errores. Si después de 3 intentos no se cumple, detente y explica el problema.
```

**Resultado:** Se verificó primero la fase en rojo (11 fallos de `test_actividades.py`). Luego se crearon `app/esquemas.py`, `app/servicios/actividades.py` y `app/rutas/actividades.py`, y se registró el router en `app/main.py`. En 1 solo intento pasaron las 19 pruebas (incluidas las 12 de aceptación) y `ruff check .` sin errores.

## Contenido inicial

**Objetivo:** cargar de forma idempotente 1 clase, 3 niños ficticios y 3 actividades de 5 preguntas del curso de Inglés.

**Herramienta y modelo:** Antigravity con Gemini 4 Hydrogen (High).

**Prompt:**

```markdown
## Rol
Actúa como desarrollador backend y diseñador de contenidos educativos para niños de 6 a 10 años.

## Objetivo
Crear en app/datos_iniciales.py la función cargar_datos_iniciales(sesion), que carga el contenido inicial del curso Inglés, y llamarla en el ciclo de vida de app/main.py después de crear_tablas().

## Contexto
Lee AGENTS.md, specs/encargo.md, specs/respuestas-cliente.md, app/modelos/__init__.py, app/main.py y tests/aceptacion/test_datos_iniciales.py.

## Restricciones
- Carga una clase con un código de 6 caracteres, 3 niños con alias de animales y avatares de la lista de specs/respuestas-cliente.md, y 3 actividades de 5 preguntas cada una, con su descripción.
- Las preguntas siguen los temas y los ejemplos de specs/encargo.md, tienen 3 o 4 opciones y una sola respuesta correcta.
- Solo carga los datos si la base de datos no tiene ninguna clase, para que al ejecutarla dos veces no se duplique nada.
- Todos los datos son ficticios y los alias no son nombres de personas.
- No modifiques ningún archivo de la carpeta tests.

## Formato de salida
Antes de escribir código, muestra los títulos de las 3 actividades y sus 15 preguntas con sus opciones y la respuesta correcta, y espera mi aprobación.

## Ejemplo
Actividad 1: «Animales en inglés». Pregunta: «¿Cómo se dice «perro» en inglés?». Opciones: Dog, Cat, Bird. Respuesta correcta: Dog.

## Criterio de éxito
python -m pytest -v pasa todas las pruebas, incluidas las de tests/aceptacion/test_datos_iniciales.py, y ruff check . no reporta errores. Si después de 3 intentos no se cumple, detente y explica el problema.
```

**Resultado:** Se verificó primero el error de importación al agregar `tests/aceptacion/test_datos_iniciales.py`. Se creó `app/datos_iniciales.py` con 3 actividades de vocabulario en inglés (Animales en inglés, Colores y números, Objetos del salón y familia), 15 preguntas revisadas sin errores y 3 niños con alias de animales. Se conectó en `app/main.py`, pasando las 21 pruebas y `ruff check .` en el primer intento.
