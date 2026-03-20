from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.base_service import BaseService
from app.core.database import get_db
from app.repositories.gym_repository import gym_repository
from app.schemas.gym_schema import GymCreate, GymUpdate, GymResponse
from app.models.usuario import Usuario


class GymService(BaseService):

    def get_all(self) -> List[GymResponse]:
        gyms = gym_repository.get_all(self.db)
        return [GymResponse.model_validate(g) for g in gyms]

    def get_mi_gym(self, current_user: Usuario) -> GymResponse:
        gym = gym_repository.get_by_id(self.db, current_user.gym_id)
        if not gym:
            raise HTTPException(status_code=404, detail="Gym no encontrado")
        return GymResponse.model_validate(gym)

    def get_by_id(self, gym_id: int) -> GymResponse:
        gym = gym_repository.get_by_id(self.db, gym_id)
        if not gym:
            raise HTTPException(status_code=404, detail="Gym no encontrado")
        return GymResponse.model_validate(gym)

    def create(self, data: GymCreate) -> GymResponse:
        gym = gym_repository.create(self.db, data)
        return GymResponse.model_validate(gym)

    def update(self, gym_id: int, data: GymUpdate, current_user: Usuario) -> GymResponse:
        self._validar_acceso_gym(current_user, gym_id)
        gym = gym_repository.get_by_id(self.db, gym_id)
        if not gym:
            raise HTTPException(status_code=404, detail="Gym no encontrado")
        updated = gym_repository.update(self.db, gym, data)
        return GymResponse.model_validate(updated)

    def deactivate(self, gym_id: int) -> dict:
        gym = gym_repository.get_by_id(self.db, gym_id)
        if not gym:
            raise HTTPException(status_code=404, detail="Gym no encontrado")
        gym_repository.deactivate(self.db, gym)
        return {"detail": "Gym desactivado correctamente"}


def get_gym_service(db: Session = Depends(get_db)) -> GymService:
    return GymService(db)