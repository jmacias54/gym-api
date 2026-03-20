from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.core.enums import UsuarioRoles
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    if payload.get("type") != "access":
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
    if usuario is None:
        raise credentials_exception
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    return usuario


def require_roles(*roles: UsuarioRoles):
    def _checker(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if current_user.rol not in [r.value for r in roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los siguientes roles: {[r.value for r in roles]}",
            )
        return current_user
    return _checker


def get_superadmin(
    current_user: Usuario = Depends(require_roles(UsuarioRoles.SUPERADMIN)),
) -> Usuario:
    return current_user


def get_admin_or_above(
    current_user: Usuario = Depends(
        require_roles(UsuarioRoles.ADMIN, UsuarioRoles.SUPERADMIN)
    ),
) -> Usuario:
    return current_user


def get_recepcion_or_above(
    current_user: Usuario = Depends(
        require_roles(UsuarioRoles.RECEPCION, UsuarioRoles.ADMIN, UsuarioRoles.SUPERADMIN)
    ),
) -> Usuario:
    return current_user


def get_current_user_gym(
    current_user: Usuario = Depends(get_current_user),
) -> int:
    if current_user.rol == UsuarioRoles.SUPERADMIN and current_user.gym_id is None:
        return None
    if current_user.gym_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario no asociado a ningún gym",
        )
    return current_user.gym_id