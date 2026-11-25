"""Punto de entrada de la aplicación FastAPI."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session

from app import proyecto
from app.datos_iniciales import cargar_datos_iniciales
from app.db import crear_tablas, motor
from app.rutas import actividades, api, paginas

CARPETA_APP = Path(__file__).resolve().parent


@asynccontextmanager
async def ciclo_vida(_app: FastAPI):
    """Inicializa las tablas y carga el contenido inicial al arrancar."""
    crear_tablas()
    with Session(motor) as sesion:
        cargar_datos_iniciales(sesion)
    yield


app = FastAPI(
    title="Plataforma lúdica de cursos para niños",
    description=f"Proyecto de {proyecto.APRENDIZ}: {proyecto.CURSO} con {proyecto.MECANICA}.",
    version=proyecto.VERSION,
    lifespan=ciclo_vida,
)

app.mount("/static", StaticFiles(directory=CARPETA_APP / "static"), name="static")
app.include_router(paginas.router)
app.include_router(api.router)
app.include_router(actividades.router)
