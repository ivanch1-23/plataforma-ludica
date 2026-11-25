"""Servicios de lógica de negocio para gestionar actividades y sus preguntas."""

from collections import defaultdict

from sqlmodel import Session, select

from app.esquemas import ActividadEntrada, ActividadSalida, PreguntaSalida
from app.modelos import Actividad, Pregunta


def _construir_salida(actividad: Actividad, preguntas: list[Pregunta]) -> ActividadSalida:
    """Construye el esquema de salida de una actividad a partir de sus modelos."""
    return ActividadSalida(
        id=actividad.id,
        titulo=actividad.titulo,
        descripcion=actividad.descripcion,
        orden=actividad.orden,
        preguntas=[PreguntaSalida.model_validate(pregunta) for pregunta in preguntas],
    )


def _obtener_preguntas_actividad(sesion: Session, actividad_id: int) -> list[Pregunta]:
    """Obtiene todas las preguntas de una actividad ordenadas por su identificador."""
    consulta = (
        select(Pregunta)
        .where(Pregunta.actividad_id == actividad_id)
        .order_by(Pregunta.id)
    )
    return list(sesion.exec(consulta).all())


def listar_actividades(sesion: Session) -> list[ActividadSalida]:
    """Devuelve todas las actividades ordenadas por el campo orden junto con sus preguntas."""
    actividades = list(sesion.exec(select(Actividad).order_by(Actividad.orden, Actividad.id)).all())
    preguntas = list(sesion.exec(select(Pregunta).order_by(Pregunta.id)).all())
    preguntas_por_actividad: dict[int, list[Pregunta]] = defaultdict(list)
    for pregunta in preguntas:
        preguntas_por_actividad[pregunta.actividad_id].append(pregunta)
    return [
        _construir_salida(actividad, preguntas_por_actividad[actividad.id])
        for actividad in actividades
        if actividad.id is not None
    ]


def obtener_actividad(sesion: Session, actividad_id: int) -> ActividadSalida | None:
    """Busca una actividad por su id o devuelve None si no existe."""
    actividad = sesion.get(Actividad, actividad_id)
    if actividad is None:
        return None
    preguntas = _obtener_preguntas_actividad(sesion, actividad_id)
    return _construir_salida(actividad, preguntas)


def crear_actividad(sesion: Session, datos: ActividadEntrada) -> ActividadSalida:
    """Crea una nueva actividad junto con todas sus preguntas."""
    actividad = Actividad(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        orden=datos.orden,
    )
    sesion.add(actividad)
    sesion.flush()

    preguntas = [
        Pregunta(
            enunciado=pregunta.enunciado,
            opciones=pregunta.opciones,
            respuesta_correcta=pregunta.respuesta_correcta,
            actividad_id=actividad.id,
        )
        for pregunta in datos.preguntas
    ]
    sesion.add_all(preguntas)
    sesion.commit()
    sesion.refresh(actividad)
    for pregunta in preguntas:
        sesion.refresh(pregunta)
    return _construir_salida(actividad, preguntas)


def actualizar_actividad(
    sesion: Session, actividad_id: int, datos: ActividadEntrada
) -> ActividadSalida | None:
    """Reemplaza los datos y preguntas de una actividad existente o devuelve None."""
    actividad = sesion.get(Actividad, actividad_id)
    if actividad is None:
        return None

    actividad.titulo = datos.titulo
    actividad.descripcion = datos.descripcion
    actividad.orden = datos.orden

    for pregunta_actual in _obtener_preguntas_actividad(sesion, actividad_id):
        sesion.delete(pregunta_actual)

    preguntas_nuevas = [
        Pregunta(
            enunciado=pregunta.enunciado,
            opciones=pregunta.opciones,
            respuesta_correcta=pregunta.respuesta_correcta,
            actividad_id=actividad_id,
        )
        for pregunta in datos.preguntas
    ]
    sesion.add_all(preguntas_nuevas)
    sesion.commit()
    sesion.refresh(actividad)
    for pregunta in preguntas_nuevas:
        sesion.refresh(pregunta)
    return _construir_salida(actividad, preguntas_nuevas)


def eliminar_actividad(sesion: Session, actividad_id: int) -> bool:
    """Elimina una actividad y todas sus preguntas; devuelve False si no existe."""
    actividad = sesion.get(Actividad, actividad_id)
    if actividad is None:
        return False

    for pregunta in _obtener_preguntas_actividad(sesion, actividad_id):
        sesion.delete(pregunta)
    sesion.delete(actividad)
    sesion.commit()
    return True
