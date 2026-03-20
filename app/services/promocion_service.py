from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.base_service import BaseService
from app.core.database import get_db
from app.repositories.promocion_repository import promocion_repository
from app.schemas.promocion_schema import PromocionCreate, PromocionUpdate, PromocionResponse
from app.models.usuario import Usuario


class PromocionService(BaseService):

    def get_all(self, current_user: Usuario) -> List[PromocionResponse]:
        promociones = promocion_repository.get_all_by_gym(self.db, current_user.gym_id)
        return [PromocionResponse.model_validate(p) for p in promociones]

    def get_activas(self, current_user: Usuario) -> List[PromocionResponse]:
        promociones = promocion_repository.get_activas_by_gym(self.db, current_user.gym_id)
        return [PromocionResponse.model_validate(p) for p in promociones]

    def get_by_id(self, promocion_id: int, current_user: Usuario) -> PromocionResponse:
        promocion = promocion_repository.get_by_id(self.db, promocion_id)
        if not promocion:
            raise HTTPException(status_code=404, detail="Promoción no encontrada")
        self._validar_acceso_gym(current_user, promocion.gym_id)
        return PromocionResponse.model_validate(promocion)

    def create(self, data: PromocionCreate, current_user: Usuario) -> PromocionResponse:
        gym_id = self._resolver_gym_id(current_user, data.gym_id)
        if data.fecha_fin < data.fecha_inicio:
            raise HTTPException(status_code=400, detail="La fecha fin no puede ser menor a la fecha inicio")
        promocion = promocion_repository.create(self.db, data, gym_id)
        return PromocionResponse.model_validate(promocion)

    def update(self, promocion_id: int, data: PromocionUpdate, current_user: Usuario) -> PromocionResponse:
        promocion = promocion_repository.get_by_id(self.db, promocion_id)
        if not promocion:
            raise HTTPException(status_code=404, detail="Promoción no encontrada")
        self._validar_acceso_gym(current_user, promocion.gym_id)
        updated = promocion_repository.update(self.db, promocion, data)
        return PromocionResponse.model_validate(updated)

    def deactivate(self, promocion_id: int, current_user: Usuario) -> dict:
        promocion = promocion_repository.get_by_id(self.db, promocion_id)
        if not promocion:
            raise HTTPException(status_code=404, detail="Promoción no encontrada")
        self._validar_acceso_gym(current_user, promocion.gym_id)
        promocion_repository.deactivate(self.db, promocion)
        return {"detail": "Promoción desactivada correctamente"}


def get_promocion_service(db: Session = Depends(get_db)) -> PromocionService:
    return PromocionService(db)