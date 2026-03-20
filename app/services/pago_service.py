from typing import List
from datetime import date, timedelta
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.base_service import BaseService
from app.core.database import get_db
from app.repositories.pago_repository import pago_repository
from app.repositories.miembro_repository import miembro_repository
from app.repositories.membresia_repository import membresia_repository
from app.repositories.promocion_repository import promocion_repository
from app.models.pago import Pago
from app.schemas.pago_schema import PagoCreate, PagoResponse, PagoResumen
from app.models.usuario import Usuario


class PagoService(BaseService):

    def _calcular_descuento(self, precio_base: float, promocion) -> tuple[float, float]:
        """Retorna (descuento_aplicado, precio_final)"""
        if not promocion:
            return 0.0, precio_base

        if promocion.tipo_descuento == "porcentaje":
            descuento = round(precio_base * float(promocion.valor_descuento) / 100, 2)
        elif promocion.tipo_descuento == "monto_fijo":
            descuento = float(promocion.valor_descuento)
        else:
            descuento = 0.0

        precio_final = max(0.0, round(precio_base - descuento, 2))
        return descuento, precio_final

    def registrar_pago(self, data: PagoCreate, current_user: Usuario) -> PagoResponse:
        gym_id = self._resolver_gym_id(current_user, data.gym_id)

        # Validar miembro
        miembro = miembro_repository.get_by_id(self.db, data.miembro_id)
        if not miembro:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        if miembro.gym_id != gym_id:
            raise HTTPException(status_code=403, detail="El miembro no pertenece a este gym")

        # Validar membresía
        membresia = membresia_repository.get_by_id(self.db, data.membresia_id)
        if not membresia:
            raise HTTPException(status_code=404, detail="Membresía no encontrada")
        if membresia.gym_id != gym_id:
            raise HTTPException(status_code=403, detail="La membresía no pertenece a este gym")
        if not membresia.activa:
            raise HTTPException(status_code=400, detail="La membresía no está activa")

        # Validar y aplicar promoción
        promocion = None
        if data.promocion_id:
            promocion = promocion_repository.get_by_id(self.db, data.promocion_id)
            if not promocion:
                raise HTTPException(status_code=404, detail="Promoción no encontrada")
            if not promocion.activa:
                raise HTTPException(status_code=400, detail="La promoción no está activa")
            if promocion.membresia_id and promocion.membresia_id != data.membresia_id:
                raise HTTPException(status_code=400, detail="La promoción no aplica para esta membresía")

        # Calcular precios
        precio_base = float(membresia.precio_base)
        descuento, precio_final = self._calcular_descuento(precio_base, promocion)

        # Calcular fechas
        fecha_inicio = date.today()
        fecha_vencimiento = fecha_inicio + timedelta(days=membresia.duracion_dias)

        # Crear pago
        pago = Pago(
            gym_id=gym_id,
            miembro_id=data.miembro_id,
            membresia_id=data.membresia_id,
            precio_original=precio_base,
            descuento_aplicado=descuento,
            precio_final=precio_final,
            metodo_pago=data.metodo_pago,
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento,
        )

        pago = pago_repository.create(self.db, pago)
        return PagoResponse.model_validate(pago)

    def get_all_by_gym(self, current_user: Usuario) -> List[PagoResponse]:
        gym_id = self._resolver_gym_id(current_user)
        pagos = pago_repository.get_all_by_gym(self.db, gym_id)
        return [PagoResponse.model_validate(p) for p in pagos]

    def get_by_miembro(self, miembro_id: int, current_user: Usuario) -> List[PagoResponse]:
        miembro = miembro_repository.get_by_id(self.db, miembro_id)
        if not miembro:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        self._validar_acceso_gym(current_user, miembro.gym_id)
        pagos = pago_repository.get_by_miembro(self.db, miembro_id)
        return [PagoResponse.model_validate(p) for p in pagos]

    def get_membresia_activa(self, miembro_id: int, current_user: Usuario) -> PagoResponse:
        miembro = miembro_repository.get_by_id(self.db, miembro_id)
        if not miembro:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        self._validar_acceso_gym(current_user, miembro.gym_id)
        pago = pago_repository.get_ultimo_pago_activo(self.db, miembro_id)
        if not pago:
            raise HTTPException(status_code=404, detail="El miembro no tiene membresía activa")
        return PagoResponse.model_validate(pago)

    def get_resumen(self, current_user: Usuario) -> PagoResumen:
        gym_id = self._resolver_gym_id(current_user)
        pagos = pago_repository.get_all_by_gym(self.db, gym_id)
        total_ingresos = sum(float(p.precio_final) for p in pagos)
        total_descuentos = sum(float(p.descuento_aplicado) for p in pagos)
        return PagoResumen(
            total_pagos=len(pagos),
            total_ingresos=round(total_ingresos, 2),
            total_descuentos=round(total_descuentos, 2),
        )


def get_pago_service(db: Session = Depends(get_db)) -> PagoService:
    return PagoService(db)