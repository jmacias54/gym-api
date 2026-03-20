from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Promocion(Base):
    __tablename__ = "promociones"
    __table_args__ = {"schema": "gym_db"}

    id = Column(Integer, primary_key=True, index=True)

    gym_id = Column(Integer, ForeignKey("gym_db.gyms.id"))
    membresia_id = Column(Integer, ForeignKey("gym_db.membresias.id"))

    nombre = Column(String(150))
    tipo_descuento = Column(String(50))

    valor_descuento = Column(Numeric(10, 2))

    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)

    activa = Column(Boolean, default=True)

    # relaciones
    gym = relationship("Gym")
    membresia = relationship("Membresia")