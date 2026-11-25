"""Conexión a la base de datos y gestión de sesiones."""

import os

from sqlmodel import Session, SQLModel, create_engine

URL_BASE_DATOS = os.getenv("DATABASE_URL", "sqlite:///./plataforma.db")
ARGUMENTOS_CONEXION = (
    {"check_same_thread": False} if URL_BASE_DATOS.startswith("sqlite") else {}
)

motor = create_engine(URL_BASE_DATOS, connect_args=ARGUMENTOS_CONEXION)


def crear_tablas() -> None:
    """Importa los modelos registrados y crea las tablas en la base de datos."""
    import app.modelos  # noqa: F401

    SQLModel.metadata.create_all(motor)


def obtener_sesion():
    """Entrega una sesión de base de datos por petición."""
    with Session(motor) as sesion:
        yield sesion
