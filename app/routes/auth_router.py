from typing import List
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user, get_admin_or_above
from app.models.usuario import Usuario
from app.schemas.auth import (
    LoginRequest, TokenResponse, RefreshRequest,
    UsuarioCreate, UsuarioUpdate, UsuarioChangePassword, UsuarioResponse,
)
from app.services.auth_service import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    return service.login(data)


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    data: RefreshRequest,
    service: AuthService = Depends(get_auth_service),
):
    return service.refresh_token(data)


@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "nombre": current_user.nombre,
        "email": current_user.email,
        "rol": current_user.rol,
        "gym_id": current_user.gym_id,
        "gym_nombre": current_user.gym.nombre if current_user.gym else None,
        "activo": current_user.activo,
    }


@router.put("/me/password")
def change_my_password(
    data: UsuarioChangePassword,
    current_user: Usuario = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
):
    return service.change_password(data, current_user)


@router.post("/usuarios", response_model=UsuarioResponse, status_code=201)
def crear_usuario(
    data: UsuarioCreate,
    current_user: Usuario = Depends(get_admin_or_above),
    service: AuthService = Depends(get_auth_service),
):
    return service.register(data, current_user)


@router.get("/usuarios", response_model=List[UsuarioResponse])
def listar_usuarios(
    current_user: Usuario = Depends(get_admin_or_above),
    service: AuthService = Depends(get_auth_service),
):
    return service.listar_usuarios(current_user)


@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    current_user: Usuario = Depends(get_admin_or_above),
    service: AuthService = Depends(get_auth_service),
):
    return service.update_usuario(usuario_id, data, current_user)


@router.delete("/usuarios/{usuario_id}")
def desactivar_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(get_admin_or_above),
    service: AuthService = Depends(get_auth_service),
):
    return service.deactivate_usuario(usuario_id, current_user)