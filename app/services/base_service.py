from typing import Optional
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.usuario import Usuario
from app.core.enums import UsuarioRoles


class BaseService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def _resolver_gym_id(self, current_user: Usuario, gym_id: Optional[int] = None) -> int:
        if current_user.rol == UsuarioRoles.SUPERADMIN:
            if not gym_id:
                raise HTTPException(status_code=400, detail="Debes especificar gym_id")
            return gym_id
        return current_user.gym_id

    def _validar_acceso_gym(self, current_user: Usuario, gym_id: int):
        if current_user.rol != UsuarioRoles.SUPERADMIN and current_user.gym_id != gym_id:
            raise HTTPException(status_code=403, detail="No tienes acceso a este recurso")