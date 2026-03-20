from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "gym_db"}

    id = Column(Integer, primary_key=True, index=True)

    gym_id = Column(Integer, ForeignKey("gym_db.gyms.id"))

    nombre = Column(String(150), nullable=False)

    email = Column(String(120), unique=True, nullable=False)

    password_hash = Column(Text, nullable=False)

    rol = Column(String(50), default="admin")

    activo = Column(Boolean, default=True)

    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # relación con gym
    gym = relationship("Gym", back_populates="usuarios")