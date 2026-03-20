from sqlalchemy import Integer, Column, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Actividad(Base):
    __tablename__ = "actividades"
    __table_args__ = {"schema": "gym_db"}

    id = Column(Integer, primary_key=True)
    gym_id = Column(Integer, ForeignKey("gym_db.gyms.id"))
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activa = Column(Boolean, default=True)

    gym = relationship("Gym", back_populates="actividades")
    membresia_actividades = relationship(
        "MembresiaActividad",
        back_populates="actividad"
    )