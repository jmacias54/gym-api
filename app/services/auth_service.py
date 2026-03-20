from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.services.base_service import BaseService
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.core.enums import UsuarioRoles
from app.repositories.usuario_repository import usuario_repository
from app.schemas.auth import (
    LoginRequest, TokenResponse, RefreshRequest,
    UsuarioCreate, UsuarioUpdate, UsuarioChangePassword, UsuarioResponse,
)
from app.models.usuario import Usuario


class AuthService(BaseService):

    def login(self, data: LoginRequest) -> TokenResponse:
        usuario = usuario_repository.get_by_email(self.db, data.email)
        if not usuario or not verify_password(data.password, usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
            )
        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo, contacta al administrador",
            )
        payload = {"sub": str(usuario.id), "gym_id": usuario.gym_id, "rol": usuario.rol}
        return TokenResponse(
            access_token=create_access_token(payload),
            refresh_token=create_refresh_token(payload),
        )

    def refresh_token(self, data: RefreshRequest) -> TokenResponse:
        payload = decode_token(data.refresh_token)
        if payload is None or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido o expirado",
            )
        usuario = usuario_repository.get_by_id(self.db, int(payload.get("sub")))
        if not usuario or not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado o inactivo",
            )
        new_payload = {"sub": str(usuario.id), "gym_id": usuario.gym_id, "rol": usuario.rol}
        return TokenResponse(
            access_token=create_access_token(new_payload),
            refresh_token=create_refresh_token(new_payload),
        )

    def register(self, data: UsuarioCreate, current_user: Usuario) -> UsuarioResponse:
        if data.rol == UsuarioRoles.SUPERADMIN and current_user.rol != UsuarioRoles.SUPERADMIN:
            raise HTTPException(status_code=403, detail="No puedes crear usuarios con rol superadmin")
        if current_user.rol == UsuarioRoles.ADMIN:
            data.gym_id = current_user.gym_id
        if usuario_repository.get_by_email(self.db, data.email):
            raise HTTPException(status_code=400, detail="Ya existe un usuario con ese email")
        usuario = usuario_repository.create(self.db, data)
        return UsuarioResponse.model_validate(usuario)

    def update_usuario(self, usuario_id: int, data: UsuarioUpdate, current_user: Usuario) -> UsuarioResponse:
        usuario = usuario_repository.get_by_id(self.db, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if current_user.rol == UsuarioRoles.ADMIN and usuario.gym_id != current_user.gym_id:
            raise HTTPException(status_code=403, detail="No tienes permiso para editar este usuario")
        updated = usuario_repository.update(self.db, usuario, data)
        return UsuarioResponse.model_validate(updated)

    def change_password(self, data: UsuarioChangePassword, current_user: Usuario) -> dict:
        if not verify_password(data.password_actual, current_user.password_hash):
            raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta")
        usuario_repository.change_password(self.db, current_user, data.password_nuevo)
        return {"detail": "Contraseña actualizada correctamente"}

    def deactivate_usuario(self, usuario_id: int, current_user: Usuario) -> dict:
        usuario = usuario_repository.get_by_id(self.db, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if usuario.id == current_user.id:
            raise HTTPException(status_code=400, detail="No puedes desactivarte a ti mismo")
        if current_user.rol == UsuarioRoles.ADMIN and usuario.gym_id != current_user.gym_id:
            raise HTTPException(status_code=403, detail="No tienes permiso")
        usuario_repository.deactivate(self.db, usuario)
        return {"detail": "Usuario desactivado correctamente"}

    def listar_usuarios(self, current_user: Usuario) -> list[UsuarioResponse]:
        if current_user.rol == UsuarioRoles.SUPERADMIN:
            usuarios = usuario_repository.get_all(self.db)
        else:
            usuarios = usuario_repository.get_all_by_gym(self.db, current_user.gym_id)
        return [UsuarioResponse.model_validate(u) for u in usuarios]


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)