"""Modelos de datos del MVP con SQLModel."""

from datetime import UTC, datetime

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class Clase(SQLModel, table=True):
    """Representa una clase escolar identificada por un código único de 6 caracteres."""

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    codigo: str = Field(max_length=6, unique=True)


class Nino(SQLModel, table=True):
    """Representa a un niño registrado en una clase mediante alias y avatar."""

    id: int | None = Field(default=None, primary_key=True)
    alias: str
    avatar: str
    clase_id: int = Field(foreign_key="clase.id")


class Actividad(SQLModel, table=True):
    """Representa una actividad de vocabulario compuesta por preguntas."""

    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    descripcion: str = Field(default="")
    orden: int


class Pregunta(SQLModel, table=True):
    """Representa una pregunta de opción múltiple asociada a una actividad."""

    id: int | None = Field(default=None, primary_key=True)
    enunciado: str
    opciones: list[str] = Field(sa_column=Column(JSON))
    respuesta_correcta: str
    actividad_id: int = Field(foreign_key="actividad.id")


class Intento(SQLModel, table=True):
    """Registra el resultado de una actividad completada por un niño."""

    id: int | None = Field(default=None, primary_key=True)
    nino_id: int = Field(foreign_key="nino.id")
    actividad_id: int = Field(foreign_key="actividad.id")
    aciertos: int
    total: int
    duracion_segundos: int
    fecha: datetime = Field(default_factory=lambda: datetime.now(UTC))
