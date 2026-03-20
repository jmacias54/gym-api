from typing import Optional
from datetime import date
from pydantic import BaseModel


class PromocionBase(BaseModel):
    nombre: str
    tipo_descuento: str  # "porcentaje" o "monto_fijo"
    valor_descuento: float
    fecha_inicio: date
    fecha_fin: date
    membresia_id: Optional[int] = None
    activa: Optional[bool] = True


class PromocionCreate(PromocionBase):
    gym_id: Optional[int] = None


class PromocionUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo_descuento: Optional[str] = None
    valor_descuento: Optional[float] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    membresia_id: Optional[int] = None
    activa: Optional[bool] = None


class PromocionResponse(PromocionBase):
    id: int
    gym_id: int

    model_config = {"from_attributes": True}