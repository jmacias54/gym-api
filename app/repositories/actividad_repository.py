from typing import List
from sqlalchemy.orm import Session
from app.models.actividad import Actividad
from app.schemas.actividad_schema import ActividadCreate, ActividadUpdate
from app.repositories.base_repository import BaseRepository


class ActividadRepository(BaseRepository[Actividad]):
    def __init__(self):
        super().__init__(Actividad)

    def get_all_by_gym(self, db: Session, gym_id: int) -> List[Actividad]:
        return db.query(Actividad).filter(Actividad.gym_id == gym_id).all()

    def get_activas_by_gym(self, db: Session, gym_id: int) -> List[Actividad]:
        return (
            db.query(Actividad)
            .filter(Actividad.gym_id == gym_id, Actividad.activa == True)
            .all()
        )

    def create(self, db: Session, data: ActividadCreate, gym_id: int) -> Actividad:
        actividad = Actividad(
            gym_id=gym_id,
            nombre=data.nombre,
            descripcion=data.descripcion,
            activa=data.activa,
        )
        db.add(actividad)
        db.commit()
        db.refresh(actividad)
        return actividad

    def update(self, db: Session, actividad: Actividad, data: ActividadUpdate) -> Actividad:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(actividad, field, value)
        db.commit()
        db.refresh(actividad)
        return actividad

    def deactivate(self, db: Session, actividad: Actividad) -> None:
        actividad.activa = False
        db.commit()


actividad_repository = ActividadRepository()