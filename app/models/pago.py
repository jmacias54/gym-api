from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime, Date
from sqlalchemy.orm import relationship

from app.core.database import Base


class Pago(Base):
    __tablename__ = "pagos"
    __table_args__ = {"schema": "gym_db"}

    id = Column(Integer, primary_key=True, index=True)

    gym_id = Column(Integer, ForeignKey("gym_db.gyms.id"))
    miembro_id = Column(Integer, ForeignKey("gym_db.miembros.id"))
    membresia_id = Column(Integer, ForeignKey("gym_db.membresias.id"))

    precio_original = Column(Numeric(10, 2))
    descuento_aplicado = Column(Numeric(10, 2))
    precio_final = Column(Numeric(10, 2))

    metodo_pago = Column(String(50))

    fecha_pago = Column(DateTime, default=datetime.utcnow)

    fecha_inicio = Column(Date)
    fecha_vencimiento = Column(Date)

    gym = relationship("Gym", back_populates="pagos")
    miembro = relationship("Miembro", back_populates="pagos")
    membresia = relationship("Membresia", back_populates="pagos")