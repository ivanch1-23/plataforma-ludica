"""Carga inicial idempotente de contenido del curso de Inglés."""

from sqlmodel import Session, select

from app.modelos import Actividad, Clase, Nino, Pregunta

ACTIVIDADES_INICIALES = [
    {
        "titulo": "Animales en inglés",
        "descripcion": "Aprende los nombres de animales conocidos en inglés.",
        "orden": 1,
        "preguntas": [
            {
                "enunciado": "¿Cómo se dice «perro» en inglés?",
                "opciones": ["Dog", "Cat", "Bird"],
                "respuesta_correcta": "Dog",
            },
            {
                "enunciado": "¿Cómo se dice «gato» en inglés?",
                "opciones": ["Fish", "Cat", "Dog", "Duck"],
                "respuesta_correcta": "Cat",
            },
            {
                "enunciado": "¿Cómo se dice «pájaro» en inglés?",
                "opciones": ["Bird", "Rabbit", "Frog"],
                "respuesta_correcta": "Bird",
            },
            {
                "enunciado": "¿Cómo se dice «pez» en inglés?",
                "opciones": ["Cow", "Horse", "Fish"],
                "respuesta_correcta": "Fish",
            },
            {
                "enunciado": "¿Cómo se dice «conejo» en inglés?",
                "opciones": ["Bear", "Rabbit", "Lion", "Duck"],
                "respuesta_correcta": "Rabbit",
            },
        ],
    },
    {
        "titulo": "Colores y números",
        "descripcion": "Practica los colores básicos y los primeros números en inglés.",
        "orden": 2,
        "preguntas": [
            {
                "enunciado": "¿Cómo se dice el color «rojo» en inglés?",
                "opciones": ["Blue", "Red", "Green"],
                "respuesta_correcta": "Red",
            },
            {
                "enunciado": "¿Cómo se dice el color «azul» en inglés?",
                "opciones": ["Blue", "Yellow", "Black", "White"],
                "respuesta_correcta": "Blue",
            },
            {
                "enunciado": "¿Cómo se dice el color «amarillo» en inglés?",
                "opciones": ["Orange", "Purple", "Yellow"],
                "respuesta_correcta": "Yellow",
            },
            {
                "enunciado": "¿Cómo se dice el número «tres» en inglés?",
                "opciones": ["One", "Two", "Three"],
                "respuesta_correcta": "Three",
            },
            {
                "enunciado": "¿Cómo se dice el número «cinco» en inglés?",
                "opciones": ["Four", "Five", "Six", "Seven"],
                "respuesta_correcta": "Five",
            },
        ],
    },
    {
        "titulo": "Objetos del salón y familia",
        "descripcion": "Identifica palabras en inglés de la familia y los útiles del salón.",
        "orden": 3,
        "preguntas": [
            {
                "enunciado": "¿Cómo se dice «libro» en inglés?",
                "opciones": ["Book", "Pencil", "Chair"],
                "respuesta_correcta": "Book",
            },
            {
                "enunciado": "¿Cómo se dice «lápiz» en inglés?",
                "opciones": ["Eraser", "Pencil", "Table", "Bag"],
                "respuesta_correcta": "Pencil",
            },
            {
                "enunciado": "¿Cómo se dice «silla» en inglés?",
                "opciones": ["Door", "Window", "Chair"],
                "respuesta_correcta": "Chair",
            },
            {
                "enunciado": "¿Cómo se dice «mamá» en inglés?",
                "opciones": ["Mother", "Father", "Sister"],
                "respuesta_correcta": "Mother",
            },
            {
                "enunciado": "¿Cómo se dice «hermano» en inglés?",
                "opciones": ["Aunt", "Brother", "Uncle", "Cousin"],
                "respuesta_correcta": "Brother",
            },
        ],
    },
]

NINOS_INICIALES = [
    {"alias": "Colibrí Veloz", "avatar": "colibri"},
    {"alias": "Jaguar Valiente", "avatar": "jaguar"},
    {"alias": "Búho Curioso", "avatar": "buho"},
]


def cargar_datos_iniciales(sesion: Session) -> None:
    """Inserta la clase, niños y actividades iniciales solo si no existen clases."""
    if sesion.exec(select(Clase)).first() is not None:
        return

    clase = Clase(nombre="Inglés Primero A", codigo="ING101")
    sesion.add(clase)
    sesion.flush()

    ninos = [
        Nino(alias=nino["alias"], avatar=nino["avatar"], clase_id=clase.id)
        for nino in NINOS_INICIALES
    ]
    sesion.add_all(ninos)

    for datos_actividad in ACTIVIDADES_INICIALES:
        actividad = Actividad(
            titulo=datos_actividad["titulo"],
            descripcion=datos_actividad["descripcion"],
            orden=datos_actividad["orden"],
        )
        sesion.add(actividad)
        sesion.flush()

        preguntas = [
            Pregunta(
                enunciado=pregunta["enunciado"],
                opciones=pregunta["opciones"],
                respuesta_correcta=pregunta["respuesta_correcta"],
                actividad_id=actividad.id,
            )
            for pregunta in datos_actividad["preguntas"]
        ]
        sesion.add_all(preguntas)

    sesion.commit()
