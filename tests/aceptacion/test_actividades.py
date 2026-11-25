"""Pruebas de aceptación: el docente gestiona las actividades del curso.

Este archivo no se modifica. El código del proyecto debe hacer pasar todas las pruebas.
"""

import pytest
from sqlmodel import select

from app.modelos import Pregunta


def preguntas_de_ejemplo(prefijo="P"):
    return [
        {
            "enunciado": f"{prefijo}{numero}: ¿cuál es la opción correcta?",
            "opciones": ["A", "B", "C"],
            "respuesta_correcta": "B",
        }
        for numero in range(1, 6)
    ]


def actividad_de_ejemplo(titulo="Actividad de prueba", orden=1):
    return {"titulo": titulo, "orden": orden, "preguntas": preguntas_de_ejemplo()}


def test_lista_vacia_cuando_no_hay_actividades(cliente):
    respuesta = cliente.get("/api/actividades")
    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_crear_actividad_con_sus_preguntas(cliente):
    respuesta = cliente.post("/api/actividades", json=actividad_de_ejemplo())
    assert respuesta.status_code == 201
    creada = respuesta.json()
    assert isinstance(creada["id"], int)
    assert creada["titulo"] == "Actividad de prueba"
    assert creada["orden"] == 1
    assert len(creada["preguntas"]) == 5
    for pregunta in creada["preguntas"]:
        assert isinstance(pregunta["id"], int)
        assert pregunta["opciones"] == ["A", "B", "C"]
        assert pregunta["respuesta_correcta"] == "B"


def test_listar_actividades_en_orden(cliente):
    cliente.post("/api/actividades", json=actividad_de_ejemplo("Segunda", orden=2))
    cliente.post("/api/actividades", json=actividad_de_ejemplo("Primera", orden=1))
    respuesta = cliente.get("/api/actividades")
    assert respuesta.status_code == 200
    assert [actividad["titulo"] for actividad in respuesta.json()] == ["Primera", "Segunda"]


def test_obtener_una_actividad(cliente):
    creada = cliente.post("/api/actividades", json=actividad_de_ejemplo()).json()
    respuesta = cliente.get(f"/api/actividades/{creada['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json()["titulo"] == "Actividad de prueba"
    assert len(respuesta.json()["preguntas"]) == 5


def test_actividad_inexistente_responde_404(cliente):
    assert cliente.get("/api/actividades/9999").status_code == 404
    assert cliente.put("/api/actividades/9999", json=actividad_de_ejemplo()).status_code == 404
    assert cliente.delete("/api/actividades/9999").status_code == 404


def test_actualizar_actividad_reemplaza_sus_preguntas(cliente, sesion):
    creada = cliente.post("/api/actividades", json=actividad_de_ejemplo()).json()
    cambios = {"titulo": "Título nuevo", "orden": 3, "preguntas": preguntas_de_ejemplo("Q")}
    respuesta = cliente.put(f"/api/actividades/{creada['id']}", json=cambios)
    assert respuesta.status_code == 200
    actualizada = cliente.get(f"/api/actividades/{creada['id']}").json()
    assert actualizada["titulo"] == "Título nuevo"
    assert actualizada["orden"] == 3
    assert all(p["enunciado"].startswith("Q") for p in actualizada["preguntas"])
    assert len(sesion.exec(select(Pregunta)).all()) == 5


def test_eliminar_actividad_y_sus_preguntas(cliente, sesion):
    creada = cliente.post("/api/actividades", json=actividad_de_ejemplo()).json()
    respuesta = cliente.delete(f"/api/actividades/{creada['id']}")
    assert respuesta.status_code == 204
    assert cliente.get(f"/api/actividades/{creada['id']}").status_code == 404
    assert sesion.exec(select(Pregunta)).all() == []


@pytest.mark.parametrize(
    "cambio",
    [
        {"titulo": ""},
        {"preguntas": preguntas_de_ejemplo()[:4]},
        {"preguntas": [{**p, "respuesta_correcta": "Z"} for p in preguntas_de_ejemplo()]},
        {"preguntas": [{**p, "opciones": ["A", "B"]} for p in preguntas_de_ejemplo()]},
        {"preguntas": [{**p, "opciones": list("ABCDE")} for p in preguntas_de_ejemplo()]},
    ],
    ids=[
        "titulo_vacio",
        "menos_de_5_preguntas",
        "respuesta_fuera_de_las_opciones",
        "menos_de_3_opciones",
        "mas_de_4_opciones",
    ],
)
def test_datos_invalidos_responden_422(cliente, cambio):
    respuesta = cliente.post("/api/actividades", json={**actividad_de_ejemplo(), **cambio})
    assert respuesta.status_code == 422
