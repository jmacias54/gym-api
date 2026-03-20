from typing import List
from sqlalchemy.orm import Session
from app.models.miembro import Miembro
from app.schemas.miembro_schema import MiembroCreate, MiembroUpdate
from app.repositories.base_repository import BaseRepository


class MiembroRepository(BaseRepository[Miembro]):
    def __init__(self):
        super().__init__(Miembro)

    def get_all_by_gym(self, db: Session, gym_id: int) -> List[Miembro]:
        return db.query(Miembro).filter(Miembro.gym_id == gym_id).all()

    def buscar(self, db: Session, gym_id: int, query: str) -> List[Miembro]:
        filtro = f"%{query}%"
        return (
            db.query(Miembro)
            .filter(
                Miembro.gym_id == gym_id,
                (
                    Miembro.nombre.ilike(filtro)
                    | Miembro.apellido.ilike(filtro)
                    | Miembro.email.ilike(filtro)
                    | Miembro.telefono.ilike(filtro)
                ),
            )
            .all()
        )

    def create(self, db: Session, data: MiembroCreate, gym_id: int) -> Miembro:
        miembro = Miembro(
            gym_id=gym_id,
            nombre=data.nombre,
            apellido=data.apellido,
            telefono=data.telefono,
            email=data.email,
            foto_url=data.foto_url,
            estado=data.estado,
        )
        db.add(miembro)
        db.commit()
        db.refresh(miembro)
        return miembro

    def update(self, db: Session, miembro: Miembro, data: MiembroUpdate) -> Miembro:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(miembro, field, value)
        db.commit()
        db.refresh(miembro)
        return miembro

    def deactivate(self, db: Session, miembro: Miembro) -> None:
        miembro.estado = "inactivo"
        db.commit()


miembro_repository = MiembroRepository()