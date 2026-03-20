from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class GymBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    activo: Optional[bool] = None


class GymCreate(GymBase):
    pass


class GymUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    activo: Optional[bool] = None


class GymResponse(GymBase):
    id: int
    activo: bool
    fecha_creacion: Optional[datetime] = None

    model_config = {"from_attributes": True}