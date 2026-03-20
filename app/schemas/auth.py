from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator

from app.core.enums import UsuarioRoles


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: Optional[UsuarioRoles] = UsuarioRoles.ADMIN
    gym_id: Optional[int] = None


class UsuarioCreate(UsuarioBase):
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v


class UsuarioUpdate(BaseModel):
    gym_id: Optional[int] = None
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    rol: Optional[UsuarioRoles] = None
    activo: Optional[bool] = None


class UsuarioChangePassword(BaseModel):
    password_actual: str
    password_nuevo: str

    @field_validator("password_nuevo")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v


class UsuarioResponse(UsuarioBase):
    id: int
    activo: Optional[bool]
    fecha_creacion: Optional[datetime] = None
    gym_nombre: Optional[str] = None
    model_config = {"from_attributes": True}