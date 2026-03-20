from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.core.security import hash_password
from app.schemas.auth import UsuarioCreate, UsuarioUpdate
from app.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self):
        super().__init__(Usuario)

    def get_by_email(self, db: Session, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()

    def get_all_by_gym(self, db: Session, gym_id: int) -> List[Usuario]:
        return db.query(Usuario).filter(Usuario.gym_id == gym_id).all()

    def create(self, db: Session, data: UsuarioCreate) -> Usuario:
        usuario = Usuario(
            gym_id=data.gym_id,
            nombre=data.nombre,
            email=data.email,
            password_hash=hash_password(data.password),
            rol=data.rol.value if data.rol else "admin",
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    def update(self, db: Session, usuario: Usuario, data: UsuarioUpdate) -> Usuario:
        payload = data.model_dump(exclude_none=True)
        if "rol" in payload and hasattr(payload["rol"], "value"):
            payload["rol"] = payload["rol"].value
        for field, value in payload.items():
            setattr(usuario, field, value)
        db.commit()
        db.refresh(usuario)
        return usuario

    def change_password(self, db: Session, usuario: Usuario, new_password: str) -> Usuario:
        usuario.password_hash = hash_password(new_password)
        db.commit()
        db.refresh(usuario)
        return usuario

    def deactivate(self, db: Session, usuario: Usuario) -> None:
        usuario.activo = False
        db.commit()


usuario_repository = UsuarioRepository()