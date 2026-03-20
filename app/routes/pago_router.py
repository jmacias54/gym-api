from typing import List
from fastapi import APIRouter, Depends
from app.core.dependencies import get_admin_or_above, get_recepcion_or_above
from app.models.usuario import Usuario
from app.schemas.pago_schema import PagoCreate, PagoResponse, PagoResumen
from app.services.pago_service import PagoService, get_pago_service

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.post("/", response_model=PagoResponse, status_code=201)
def registrar_pago(
    data: PagoCreate,
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: PagoService = Depends(get_pago_service),
):
    """Registra un pago y renueva la membresía del miembro."""
    return service.registrar_pago(data, current_user)


@router.get("/", response_model=List[PagoResponse])
def listar_pagos(
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: PagoService = Depends(get_pago_service),
):
    return service.get_all_by_gym(current_user)


@router.get("/resumen", response_model=PagoResumen)
def resumen_pagos(
    current_user: Usuario = Depends(get_admin_or_above),
    service: PagoService = Depends(get_pago_service),
):
    """Resumen total de ingresos y descuentos del gym."""
    return service.get_resumen(current_user)


@router.get("/miembro/{miembro_id}", response_model=List[PagoResponse])
def historial_miembro(
    miembro_id: int,
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: PagoService = Depends(get_pago_service),
):
    """Historial de pagos de un miembro."""
    return service.get_by_miembro(miembro_id, current_user)


@router.get("/miembro/{miembro_id}/activa", response_model=PagoResponse)
def membresia_activa(
    miembro_id: int,
    current_user: Usuario = Depends(get_recepcion_or_above),
    service: PagoService = Depends(get_pago_service),
):
    """Verifica si un miembro tiene membresía vigente."""
    return service.get_membresia_activa(miembro_id, current_user)