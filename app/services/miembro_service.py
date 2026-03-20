from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.base_service import BaseService
from app.core.database import get_db
from app.repositories.miembro_repository import miembro_repository
from app.repositories.gym_repository import gym_repository
from app.schemas.miembro_schema import MiembroCreate, MiembroUpdate, MiembroResponse
from app.models.usuario import Usuario
from app.core.enums import UsuarioRoles


class MiembroService(BaseService):

    def get_all(self, current_user: Usuario) -> List[MiembroResponse]:
        if current_user.rol == UsuarioRoles.SUPERADMIN:
            miembros = miembro_repository.get_all(self.db)
        else:
            miembros = miembro_repository.get_all_by_gym(self.db, current_user.gym_id)
        return [MiembroResponse.model_validate(m) for m in miembros]

    def buscar(self, query: str, current_user: Usuario) -> List[MiembroResponse]:
        gym_id = self._resolver_gym_id(current_user)
        miembros = miembro_repository.buscar(self.db, gym_id, query)
        return [MiembroResponse.model_validate(m) for m in miembros]

    def get_by_id(self, miembro_id: int, current_user: Usuario) -> MiembroResponse:
        miembro = miembro_repository.get_by_id(self.db, miembro_id)
        if not miembro:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        self._validar_acceso_gym(current_user, miembro.gym_id)
        return MiembroResponse.model_validate(miembro)

    def create(self, data: MiembroCreate, current_user: Usuario) -> MiembroResponse:
        gym_id = self._resolver_gym_id(current_user, data.gym_id)
        if not gym_repository.get_by_id(self.db, gym_id):
            raise HTTPException(status_code=404, detail="Gym no encontrado")
        miembro = miembro_repository.create(self.db, data, gym_id)
        return MiembroResponse.model_validate(miembro)

    def update(self, miembro_id: int, data: MiembroUpdate, current_user: Usuario) -> MiembroResponse:
        miembro = miembro_repository.get_by_id(self.db, miembro_id)
        if not miembro:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        self._validar_acceso_gym(current_user, miembro.gym_id)
        updated = miembro_repository.update(self.db, miembro, data)
        return MiembroResponse.model_validate(updated)

    def deactivate(self, miembro_id: int, current_user: Usuario) -> dict:
        miembro = miembro_repository.get_by_id(self.db, miembro_id)
        if not miembro:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        self._validar_acceso_gym(current_user, miembro.gym_id)
        miembro_repository.deactivate(self.db, miembro)
        return {"detail": "Miembro desactivado correctamente"}


def get_miembro_service(db: Session = Depends(get_db)) -> MiembroService:
    return MiembroService(db)