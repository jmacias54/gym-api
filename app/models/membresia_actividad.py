from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class MembresiaActividad(Base):
    __tablename__ = "membresia_actividades"
    __table_args__ = {"schema": "gym_db"}

    id = Column(Integer, primary_key=True, index=True)

    membresia_id = Column(Integer, ForeignKey("gym_db.membresias.id"))
    actividad_id = Column(Integer, ForeignKey("gym_db.actividades.id"))

    # relaciones
    membresia = relationship("Membresia", back_populates="membresia_actividades")
    actividad = relationship("Actividad", back_populates="membresia_actividades")