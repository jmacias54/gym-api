from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.base_service import BaseService
from app.core.database import get_db
from app.repositories.actividad_repository import actividad_repository
from app.schemas.actividad_schema import ActividadCreate, ActividadUpdate, ActividadResponse
from app.models.usuario import Usuario


class ActividadService(BaseService):

    def get_all(self, current_user: Usuario) -> List[ActividadResponse]:
        actividades = actividad_repository.get_all_by_gym(self.db, current_user.gym_id)
        return [ActividadResponse.model_validate(a) for a in actividades]

    def get_by_id(self, actividad_id: int, current_user: Usuario) -> ActividadResponse:
        actividad = actividad_repository.get_by_id(self.db, actividad_id)
        if not actividad:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        self._validar_acceso_gym(current_user, actividad.gym_id)
        return ActividadResponse.model_validate(actividad)

    def create(self, data: ActividadCreate, current_user: Usuario) -> ActividadResponse:
        gym_id = self._resolver_gym_id(current_user, data.gym_id)
        actividad = actividad_repository.create(self.db, data, gym_id)
        return ActividadResponse.model_validate(actividad)

    def update(self, actividad_id: int, data: ActividadUpdate, current_user: Usuario) -> ActividadResponse:
        actividad = actividad_repository.get_by_id(self.db, actividad_id)
        if not actividad:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        self._validar_acceso_gym(current_user, actividad.gym_id)
        updated = actividad_repository.update(self.db, actividad, data)
        return ActividadResponse.model_validate(updated)

    def deactivate(self, actividad_id: int, current_user: Usuario) -> dict:
        actividad = actividad_repository.get_by_id(self.db, actividad_id)
        if not actividad:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        self._validar_acceso_gym(current_user, actividad.gym_id)
        actividad_repository.deactivate(self.db, actividad)
        return {"detail": "Actividad desactivada correctamente"}


def get_actividad_service(db: Session = Depends(get_db)) -> ActividadService:
    return ActividadService(db)