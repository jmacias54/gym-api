from typing import List
from sqlalchemy.orm import Session
from app.models.gym import Gym
from app.schemas.gym_schema import GymCreate, GymUpdate
from app.repositories.base_repository import BaseRepository


class GymRepository(BaseRepository[Gym]):
    def __init__(self):
        super().__init__(Gym)

    def get_activos(self, db: Session) -> List[Gym]:
        return db.query(Gym).filter(Gym.activo == True).all()

    def create(self, db: Session, data: GymCreate) -> Gym:
        gym = Gym(**data.model_dump())
        db.add(gym)
        db.commit()
        db.refresh(gym)
        return gym

    def update(self, db: Session, gym: Gym, data: GymUpdate) -> Gym:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(gym, field, value)
        db.commit()
        db.refresh(gym)
        return gym

    def deactivate(self, db: Session, gym: Gym) -> None:
        gym.activo = False
        db.commit()


gym_repository = GymRepository()