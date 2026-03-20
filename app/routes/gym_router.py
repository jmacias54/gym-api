from typing import List
from fastapi import APIRouter, Depends
from app.core.dependencies import get_admin_or_above, get_superadmin
from app.models.usuario import Usuario
from app.schemas.gym_schema import GymCreate, GymUpdate, GymResponse
from app.services.gym_service import GymService, get_gym_service

router = APIRouter(prefix="/gyms", tags=["Gyms"])


@router.get("/mi-gym", response_model=GymResponse)
def mi_gym(
    current_user: Usuario = Depends(get_admin_or_above),
    service: GymService = Depends(get_gym_service),
):
    return service.get_mi_gym(current_user)


@router.get("/", response_model=List[GymResponse])
def listar_gyms(
    _: Usuario = Depends(get_superadmin),
    service: GymService = Depends(get_gym_service),
):
    return service.get_all()


@router.get("/{gym_id}", response_model=GymResponse)
def obtener_gym(
    gym_id: int,
    _: Usuario = Depends(get_admin_or_above),
    service: GymService = Depends(get_gym_service),
):
    return service.get_by_id(gym_id)


@router.post("/", response_model=GymResponse, status_code=201)
def crear_gym(
    data: GymCreate,
    _: Usuario = Depends(get_superadmin),
    service: GymService = Depends(get_gym_service),
):
    return service.create(data)


@router.put("/{gym_id}", response_model=GymResponse)
def actualizar_gym(
    gym_id: int,
    data: GymUpdate,
    current_user: Usuario = Depends(get_admin_or_above),
    service: GymService = Depends(get_gym_service),
):
    return service.update(gym_id, data, current_user)


@router.delete("/{gym_id}")
def desactivar_gym(
    gym_id: int,
    _: Usuario = Depends(get_superadmin),
    service: GymService = Depends(get_gym_service),
):
    return service.deactivate(gym_id)