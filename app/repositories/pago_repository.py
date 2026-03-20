from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session, joinedload
from app.models.pago import Pago
from app.repositories.base_repository import BaseRepository


class PagoRepository(BaseRepository[Pago]):
    def __init__(self):
        super().__init__(Pago)

    def get_all_by_gym(self, db: Session, gym_id: int) -> List[Pago]:
        return (
            db.query(Pago)
            .options(joinedload(Pago.miembro), joinedload(Pago.membresia))
            .filter(Pago.gym_id == gym_id)
            .order_by(Pago.fecha_pago.desc())
            .all()
        )

    def get_by_miembro(self, db: Session, miembro_id: int) -> List[Pago]:
        return (
            db.query(Pago)
            .options(joinedload(Pago.membresia))
            .filter(Pago.miembro_id == miembro_id)
            .order_by(Pago.fecha_pago.desc())
            .all()
        )

    def get_ultimo_pago_activo(self, db: Session, miembro_id: int) -> Optional[Pago]:
        hoy = date.today()
        return (
            db.query(Pago)
            .filter(
                Pago.miembro_id == miembro_id,
                Pago.fecha_vencimiento >= hoy,
            )
            .order_by(Pago.fecha_vencimiento.desc())
            .first()
        )

    def create(self, db: Session, pago: Pago) -> Pago:
        db.add(pago)
        db.commit()
        db.refresh(pago)
        return pago


pago_repository = PagoRepository()