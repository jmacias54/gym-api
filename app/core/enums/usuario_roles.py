from enum import Enum


class UsuarioRoles(str, Enum):
    SUPERADMIN = "superadmin"  # Acceso total, ve todos los gyms
    ADMIN = "admin"            # Administrador del gym
    RECEPCION = "recepcion"    # Solo operaciones básicas