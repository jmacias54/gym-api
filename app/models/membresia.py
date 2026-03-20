from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Membresia(Base):
    __tablename__ = "membresias"
    __table_args__ = {"schema": "gym_db"}

    id = Column(Integer, primary_key=True, index=True)
    gym_id = Column(Integer, ForeignKey("gym_db.gyms.id"))
    nombre = Column(String(100), nullable=False)
    duracion_dias = Column(Integer, nullable=False)
    precio_base = Column(Integer, nullable=False)
    activa = Column(Boolean, default=True)

    gym = relationship("Gym", back_populates="membresias")
    pagos = relationship("Pago", back_populates="membresia")
    membresia_actividades = relationship(
        "MembresiaActividad",
        back_populates="membresia"
    )

