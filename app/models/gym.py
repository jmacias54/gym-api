from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base
from datetime import datetime

class Gym(Base):
    __tablename__ = "gyms"
    __table_args__ = {"schema": "gym_db"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String)
    telefono = Column(String)
    email = Column(String)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    miembros = relationship("Miembro", back_populates="gym")
    actividades = relationship("Actividad", back_populates="gym")
    usuarios = relationship("Usuario", back_populates="gym")
    membresias = relationship("Membresia", back_populates="gym")
    pagos = relationship("Pago", back_populates="gym")