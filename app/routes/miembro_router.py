from typing import List
from fastapi import APIRouter, Depends, Query
from app.core.dependencies import get_current_user, get_admin_or_above, get_recepcion_or_above
from app.models.usuario import Usuario
from app.schemas.miembro_schema import MiembroCreate, MiembroUpdate, MiembroResponse
from app.services.miembro_service import MiembroService, get_miembro_service

router = APIRouter(prefix="/miembros", tags=["Miembros"])


@router.get("/", response_model=List[MiembroResponse])
def listar_miembros(
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: MiembroService = Depends(get_miembro_service),
):
    return service.get_all(current_user)


@router.get("/buscar", response_model=List[MiembroResponse])
def buscar_miembros(
    q: str = Query(..., min_length=2, description="Nombre, apellido, email o teléfono"),
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: MiembroService = Depends(get_miembro_service),
):
    return service.buscar(q, current_user)


@router.get("/{miembro_id}", response_model=MiembroResponse)
def obtener_miembro(
    miembro_id: int,
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: MiembroService = Depends(get_miembro_service),
):
    return service.get_by_id(miembro_id, current_user)


@router.post("/", response_model=MiembroResponse, status_code=201)
def crear_miembro(
    data: MiembroCreate,
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: MiembroService = Depends(get_miembro_service),
):
    return service.create(data, current_user)


@router.put("/{miembro_id}", response_model=MiembroResponse)
def actualizar_miembro(
    miembro_id: int,
    data: MiembroUpdate,
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: MiembroService = Depends(get_miembro_service),
):
    return service.update(miembro_id, data, current_user)


@router.delete("/{miembro_id}")
def desactivar_miembro(
    miembro_id: int,
    current_user: Usuario = Depends(get_admin_or_above),
    service: MiembroService = Depends(get_miembro_service),
):
    return service.deactivate(miembro_id, current_user)