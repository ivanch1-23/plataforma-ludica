"""Pruebas de aceptación: la plataforma inicia con contenido del curso.

Este archivo no se modifica. El código del proyecto debe hacer pasar todas las pruebas.
"""

from sqlmodel import select

from app.datos_iniciales import cargar_datos_iniciales
from app.modelos import Actividad, Clase, Nino, Pregunta


def test_carga_inicial_crea_clase_ninos_y_actividades(sesion):
    cargar_datos_iniciales(sesion)
    clases = sesion.exec(select(Clase)).all()
    assert len(clases) == 1
    assert len(clases[0].codigo) == 6
    ninos = sesion.exec(select(Nino)).all()
    assert len(ninos) == 3
    assert all(nino.clase_id == clases[0].id and nino.alias and nino.avatar for nino in ninos)
    actividades = sesion.exec(select(Actividad)).all()
    assert len(actividades) == 3
    for actividad in actividades:
        preguntas = sesion.exec(
            select(Pregunta).where(Pregunta.actividad_id == actividad.id)
        ).all()
        assert len(preguntas) >= 5
        for pregunta in preguntas:
            assert 3 <= len(pregunta.opciones) <= 4
            assert pregunta.respuesta_correcta in pregunta.opciones


def test_carga_inicial_no_duplica_los_datos(sesion):
    cargar_datos_iniciales(sesion)
    cargar_datos_iniciales(sesion)
    assert len(sesion.exec(select(Clase)).all()) == 1
    assert len(sesion.exec(select(Nino)).all()) == 3
    assert len(sesion.exec(select(Actividad)).all()) == 3
