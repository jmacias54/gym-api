from typing import List
from fastapi import APIRouter, Depends
from app.core.dependencies import get_admin_or_above, get_recepcion_or_above
from app.models.usuario import Usuario
from app.schemas.actividad_schema import ActividadCreate, ActividadUpdate, ActividadResponse
from app.services.actividad_service import ActividadService, get_actividad_service

router = APIRouter(prefix="/actividades", tags=["Actividades"])


@router.get("/", response_model=List[ActividadResponse])
def listar_actividades(
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: ActividadService = Depends(get_actividad_service),
):
    return service.get_all(current_user)


@router.get("/{actividad_id}", response_model=ActividadResponse)
def obtener_actividad(
    actividad_id: int,
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: ActividadService = Depends(get_actividad_service),
):
    return service.get_by_id(actividad_id, current_user)


@router.post("/", response_model=ActividadResponse, status_code=201)
def crear_actividad(
    data: ActividadCreate,
    current_user: Usuario = Depends(get_admin_or_above),
    service: ActividadService = Depends(get_actividad_service),
):
    return service.create(data, current_user)


@router.put("/{actividad_id}", response_model=ActividadResponse)
def actualizar_actividad(
    actividad_id: int,
    data: ActividadUpdate,
    current_user: Usuario = Depends(get_admin_or_above),
    service: ActividadService = Depends(get_actividad_service),
):
    return service.update(actividad_id, data, current_user)


@router.delete("/{actividad_id}")
def desactivar_actividad(
    actividad_id: int,
    current_user: Usuario = Depends(get_admin_or_above),
    service: ActividadService = Depends(get_actividad_service),
):
    return service.deactivate(actividad_id, current_user)