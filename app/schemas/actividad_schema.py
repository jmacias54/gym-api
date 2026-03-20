from typing import Optional
from pydantic import BaseModel


class ActividadBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activa: Optional[bool] = True


class ActividadCreate(ActividadBase):
    gym_id: Optional[int] = None


class ActividadUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activa: Optional[bool] = None


class ActividadResponse(ActividadBase):
    id: int
    gym_id: int

    model_config = {"from_attributes": True}