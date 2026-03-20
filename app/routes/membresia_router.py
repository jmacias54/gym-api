from typing import List
from fastapi import APIRouter, Depends
from app.core.dependencies import get_admin_or_above, get_recepcion_or_above
from app.models.usuario import Usuario
from app.schemas.membresia_scheme import MembresiaCreate, MembresiaUpdate, MembresiaResponse
from app.services.membresia_service import MembresiaService, get_membresia_service

router = APIRouter(prefix="/membresias", tags=["Membresías"])


@router.get("/", response_model=List[MembresiaResponse])
def listar_membresias(
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: MembresiaService = Depends(get_membresia_service),
):
    return service.get_all(current_user)


@router.get("/{membresia_id}", response_model=MembresiaResponse)
def obtener_membresia(
    membresia_id: int,
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: MembresiaService = Depends(get_membresia_service),
):
    return service.get_by_id(membresia_id, current_user)


@router.post("/", response_model=MembresiaResponse, status_code=201)
def crear_membresia(
    data: MembresiaCreate,
    current_user: Usuario = Depends(get_admin_or_above),
    service: MembresiaService = Depends(get_membresia_service),
):
    return service.create(data, current_user)


@router.put("/{membresia_id}", response_model=MembresiaResponse)
def actualizar_membresia(
    membresia_id: int,
    data: MembresiaUpdate,
    current_user: Usuario = Depends(get_admin_or_above),
    service: MembresiaService = Depends(get_membresia_service),
):
    return service.update(membresia_id, data, current_user)


@router.delete("/{membresia_id}")
def desactivar_membresia(
    membresia_id: int,
    current_user: Usuario = Depends(get_admin_or_above),
    service: MembresiaService = Depends(get_membresia_service),
):
    return service.deactivate(membresia_id, current_user)