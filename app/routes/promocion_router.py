from typing import List
from fastapi import APIRouter, Depends
from app.core.dependencies import get_admin_or_above, get_recepcion_or_above
from app.models.usuario import Usuario
from app.schemas.promocion_schema import PromocionCreate, PromocionUpdate, PromocionResponse
from app.services.promocion_service import PromocionService, get_promocion_service

router = APIRouter(prefix="/promociones", tags=["Promociones"])


@router.get("/", response_model=List[PromocionResponse])
def listar_promociones(
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: PromocionService = Depends(get_promocion_service),
):
    return service.get_all(current_user)


@router.get("/activas", response_model=List[PromocionResponse])
def listar_activas(
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: PromocionService = Depends(get_promocion_service),
):
    return service.get_activas(current_user)


@router.get("/{promocion_id}", response_model=PromocionResponse)
def obtener_promocion(
    promocion_id: int,
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: PromocionService = Depends(get_promocion_service),
):
    return service.get_by_id(promocion_id, current_user)


@router.post("/", response_model=PromocionResponse, status_code=201)
def crear_promocion(
    data: PromocionCreate,
    current_user: Usuario = Depends(get_admin_or_above),
    service: PromocionService = Depends(get_promocion_service),
):
    return service.create(data, current_user)


@router.put("/{promocion_id}", response_model=PromocionResponse)
def actualizar_promocion(
    promocion_id: int,
    data: PromocionUpdate,
    current_user: Usuario = Depends(get_admin_or_above),
    service: PromocionService = Depends(get_promocion_service),
):
    return service.update(promocion_id, data, current_user)


@router.delete("/{promocion_id}")
def desactivar_promocion(
    promocion_id: int,
    current_user: Usuario = Depends(get_admin_or_above),
    service: PromocionService = Depends(get_promocion_service),
):
    return service.deactivate(promocion_id, current_user)