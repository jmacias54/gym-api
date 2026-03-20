from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.membresia import Membresia
from app.models.membresia_actividad import MembresiaActividad
from app.schemas.membresia_scheme import MembresiaCreate, MembresiaUpdate
from app.repositories.base_repository import BaseRepository


class MembresiaRepository(BaseRepository[Membresia]):
    def __init__(self):
        super().__init__(Membresia)

    def get_by_id(self, db: Session, membresia_id: int) -> Optional[Membresia]:
        return (
            db.query(Membresia)
            .options(
                joinedload(Membresia.membresia_actividades)
                .joinedload(MembresiaActividad.actividad)
            )
            .filter(Membresia.id == membresia_id)
            .first()
        )

    def get_all_by_gym(self, db: Session, gym_id: int) -> List[Membresia]:
        return (
            db.query(Membresia)
            .options(
                joinedload(Membresia.membresia_actividades)
                .joinedload(MembresiaActividad.actividad)
            )
            .filter(Membresia.gym_id == gym_id)
            .all()
        )

    def create(self, db: Session, data: MembresiaCreate, gym_id: int) -> Membresia:
        membresia = Membresia(
            gym_id=gym_id,
            nombre=data.nombre,
            duracion_dias=data.duracion_dias,
            precio_base=data.precio_base,
            activa=data.activa,
        )
        db.add(membresia)
        db.flush()  # obtenemos el id antes del commit

        if data.actividad_ids:
            for actividad_id in data.actividad_ids:
                db.add(MembresiaActividad(
                    membresia_id=membresia.id,
                    actividad_id=actividad_id,
                ))

        db.commit()
        db.refresh(membresia)
        return membresia

    def update(self, db: Session, membresia: Membresia, data: MembresiaUpdate) -> Membresia:
        payload = data.model_dump(exclude_none=True)
        actividad_ids = payload.pop("actividad_ids", None)

        for field, value in payload.items():
            setattr(membresia, field, value)

        if actividad_ids is not None:
            db.query(MembresiaActividad).filter(
                MembresiaActividad.membresia_id == membresia.id
            ).delete()
            for actividad_id in actividad_ids:
                db.add(MembresiaActividad(
                    membresia_id=membresia.id,
                    actividad_id=actividad_id,
                ))

        db.commit()
        db.refresh(membresia)
        return membresia

    def deactivate(self, db: Session, membresia: Membresia) -> None:
        membresia.activa = False
        db.commit()


membresia_repository = MembresiaRepository()