"""Configuración compartida de las pruebas de aceptación.

Cada prueba usa una base de datos nueva en memoria, sin tocar plataforma.db.
Este archivo no se modifica.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.db import obtener_sesion
from app.main import app


@pytest.fixture
def sesion():
    motor = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(motor)
    with Session(motor) as sesion:
        yield sesion


@pytest.fixture
def cliente(sesion):
    app.dependency_overrides[obtener_sesion] = lambda: sesion
    yield TestClient(app)
    app.dependency_overrides.clear()
