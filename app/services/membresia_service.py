from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.base_service import BaseService
from app.core.database import get_db
from app.repositories.membresia_repository import membresia_repository
from app.repositories.actividad_repository import actividad_repository
from app.schemas.membresia_scheme import MembresiaCreate, MembresiaUpdate, MembresiaResponse
from app.models.usuario import Usuario


class MembresiaService(BaseService):

    def _validar_actividades(self, actividad_ids: List[int], gym_id: int):
        for actividad_id in actividad_ids:
            actividad = actividad_repository.get_by_id(self.db, actividad_id)
            if not actividad:
                raise HTTPException(status_code=404, detail=f"Actividad {actividad_id} no encontrada")
            if actividad.gym_id != gym_id:
                raise HTTPException(status_code=400, detail=f"Actividad {actividad_id} no pertenece a este gym")

    def get_all(self, current_user: Usuario) -> List[MembresiaResponse]:
        membresias = membresia_repository.get_all_by_gym(self.db, current_user.gym_id)
        return [MembresiaResponse.model_validate(m) for m in membresias]

    def get_by_id(self, membresia_id: int, current_user: Usuario) -> MembresiaResponse:
        membresia = membresia_repository.get_by_id(self.db, membresia_id)
        if not membresia:
            raise HTTPException(status_code=404, detail="Membresía no encontrada")
        self._validar_acceso_gym(current_user, membresia.gym_id)
        return MembresiaResponse.model_validate(membresia)

    def create(self, data: MembresiaCreate, current_user: Usuario) -> MembresiaResponse:
        gym_id = self._resolver_gym_id(current_user, data.gym_id)
        if data.actividad_ids:
            self._validar_actividades(data.actividad_ids, gym_id)
        membresia = membresia_repository.create(self.db, data, gym_id)
        return MembresiaResponse.model_validate(membresia)

    def update(self, membresia_id: int, data: MembresiaUpdate, current_user: Usuario) -> MembresiaResponse:
        membresia = membresia_repository.get_by_id(self.db, membresia_id)
        if not membresia:
            raise HTTPException(status_code=404, detail="Membresía no encontrada")
        self._validar_acceso_gym(current_user, membresia.gym_id)
        if data.actividad_ids:
            self._validar_actividades(data.actividad_ids, membresia.gym_id)
        updated = membresia_repository.update(self.db, membresia, data)
        return MembresiaResponse.model_validate(updated)

    def deactivate(self, membresia_id: int, current_user: Usuario) -> dict:
        membresia = membresia_repository.get_by_id(self.db, membresia_id)
        if not membresia:
            raise HTTPException(status_code=404, detail="Membresía no encontrada")
        self._validar_acceso_gym(current_user, membresia.gym_id)
        membresia_repository.deactivate(self.db, membresia)
        return {"detail": "Membresía desactivada correctamente"}


def get_membresia_service(db: Session = Depends(get_db)) -> MembresiaService:
    return MembresiaService(db)