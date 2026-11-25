"""Rutas HTTP para gestionar las actividades del curso."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db import obtener_sesion
from app.esquemas import ActividadEntrada, ActividadSalida
from app.servicios import actividades as servicio_actividades

router = APIRouter(prefix="/api/actividades", tags=["Actividades"])

SesionDep = Annotated[Session, Depends(obtener_sesion)]


@router.get("", response_model=list[ActividadSalida])
def listar_actividades(sesion: SesionDep):
    """Lista todas las actividades ordenadas por el campo orden."""
    return servicio_actividades.listar_actividades(sesion)


@router.post("", response_model=ActividadSalida, status_code=status.HTTP_201_CREATED)
def crear_actividad(datos: ActividadEntrada, sesion: SesionDep):
    """Crea una actividad con sus preguntas."""
    return servicio_actividades.crear_actividad(sesion, datos)


@router.get("/{actividad_id}", response_model=ActividadSalida)
def obtener_actividad(actividad_id: int, sesion: SesionDep):
    """Obtiene una actividad por su identificador."""
    actividad = servicio_actividades.obtener_actividad(sesion, actividad_id)
    if actividad is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada.",
        )
    return actividad


@router.put("/{actividad_id}", response_model=ActividadSalida)
def actualizar_actividad(actividad_id: int, datos: ActividadEntrada, sesion: SesionDep):
    """Actualiza una actividad existente y reemplaza sus preguntas."""
    actividad = servicio_actividades.actualizar_actividad(sesion, actividad_id, datos)
    if actividad is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada.",
        )
    return actividad


@router.delete("/{actividad_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_actividad(actividad_id: int, sesion: SesionDep):
    """Elimina una actividad y sus preguntas asociadas."""
    eliminada = servicio_actividades.eliminar_actividad(sesion, actividad_id)
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada.",
        )
