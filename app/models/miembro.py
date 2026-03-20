from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Miembro(Base):
    __tablename__ = "miembros"
    __table_args__ = {"schema": "gym_db"}

    id = Column(Integer, primary_key=True, index=True)

    gym_id = Column(Integer, ForeignKey("gym_db.gyms.id"))

    nombre = Column(String(150), nullable=False)
    apellido = Column(String(150), nullable=False)
    telefono = Column(String(20))
    email = Column(String(120))

    foto_url = Column(Text)

    estado = Column(String(50), default="activo")

    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # relación con gym
    gym = relationship("Gym", back_populates="miembros")
    pagos = relationship("Pago", back_populates="miembro")
