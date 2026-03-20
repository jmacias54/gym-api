from typing import Optional, List
from pydantic import BaseModel
from app.schemas.actividad_schema import ActividadResponse


class MembresiaBase(BaseModel):
    nombre: str
    duracion_dias: int
    precio_base: float
    activa: Optional[bool] = True


class MembresiaCreate(MembresiaBase):
    gym_id: Optional[int] = None
    actividad_ids: Optional[List[int]] = []


class MembresiaUpdate(BaseModel):
    nombre: Optional[str] = None
    duracion_dias: Optional[int] = None
    precio_base: Optional[float] = None
    activa: Optional[bool] = None
    actividad_ids: Optional[List[int]] = None


class MembresiaResponse(MembresiaBase):
    id: int
    gym_id: int
    actividades: Optional[List[ActividadResponse]] = []

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        data = super().model_validate(obj, **kwargs)
        # Extrae actividades desde la tabla pivote membresia_actividades
        data.actividades = [
            ActividadResponse.model_validate(ma.actividad)
            for ma in obj.membresia_actividades
            if ma.actividad
        ]
        return data