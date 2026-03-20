from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class MiembroBase(BaseModel):
    nombre: str
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    foto_url: Optional[str] = None
    estado: Optional[str] = "activo"


class MiembroCreate(MiembroBase):
    gym_id: Optional[int] = None  # Se toma del token si es admin


class MiembroUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    foto_url: Optional[str] = None
    estado: Optional[str] = None


class MiembroResponse(MiembroBase):
    id: int
    gym_id: int
    fecha_registro: Optional[datetime] = None

    model_config = {"from_attributes": True}