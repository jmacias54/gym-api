from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel


class PagoCreate(BaseModel):
    miembro_id: int
    membresia_id: int
    metodo_pago: str  # "efectivo", "tarjeta", "transferencia"
    promocion_id: Optional[int] = None
    gym_id: Optional[int] = None


class PagoResponse(BaseModel):
    id: int
    gym_id: int
    miembro_id: int
    membresia_id: int
    precio_original: float
    descuento_aplicado: float
    precio_final: float
    metodo_pago: str
    fecha_pago: Optional[datetime] = None
    fecha_inicio: Optional[date] = None
    fecha_vencimiento: Optional[date] = None

    model_config = {"from_attributes": True}


class PagoResumen(BaseModel):
    """Para reportes y dashboard"""
    total_pagos: int
    total_ingresos: float
    total_descuentos: float