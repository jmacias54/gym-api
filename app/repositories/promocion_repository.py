from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from app.models.promocion import Promocion
from app.schemas.promocion_schema import PromocionCreate, PromocionUpdate
from app.repositories.base_repository import BaseRepository


class PromocionRepository(BaseRepository[Promocion]):
    def __init__(self):
        super().__init__(Promocion)

    def get_all_by_gym(self, db: Session, gym_id: int) -> List[Promocion]:
        return db.query(Promocion).filter(Promocion.gym_id == gym_id).all()

    def get_activas_by_gym(self, db: Session, gym_id: int) -> List[Promocion]:
        hoy = date.today()
        return (
            db.query(Promocion)
            .filter(
                Promocion.gym_id == gym_id,
                Promocion.activa == True,
                Promocion.fecha_inicio <= hoy,
                Promocion.fecha_fin >= hoy,
            )
            .all()
        )

    def get_activas_by_membresia(self, db: Session, gym_id: int, membresia_id: int) -> List[Promocion]:
        hoy = date.today()
        return (
            db.query(Promocion)
            .filter(
                Promocion.gym_id == gym_id,
                Promocion.activa == True,
                Promocion.fecha_inicio <= hoy,
                Promocion.fecha_fin >= hoy,
                Promocion.membresia_id == membresia_id,
            )
            .all()
        )

    def create(self, db: Session, data: PromocionCreate, gym_id: int) -> Promocion:
        promocion = Promocion(
            gym_id=gym_id,
            nombre=data.nombre,
            tipo_descuento=data.tipo_descuento,
            valor_descuento=data.valor_descuento,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin,
            membresia_id=data.membresia_id,
            activa=data.activa,
        )
        db.add(promocion)
        db.commit()
        db.refresh(promocion)
        return promocion

    def update(self, db: Session, promocion: Promocion, data: PromocionUpdate) -> Promocion:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(promocion, field, value)
        db.commit()
        db.refresh(promocion)
        return promocion

    def deactivate(self, db: Session, promocion: Promocion) -> None:
        promocion.activa = False
        db.commit()


promocion_repository = PromocionRepository()