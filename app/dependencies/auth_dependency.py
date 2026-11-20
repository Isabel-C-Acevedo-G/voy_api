"""Dependencias de autenticación y autorización (OAuth2 + roles)."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token
from app.dependencies.database_dependency import get_db
from app.models.usuario_model import Usuario
from app.services import rol_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    correo = payload.get("sub")
    if not correo:
        raise credentials_exception
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if usuario is None:
        raise credentials_exception
    return usuario


def get_current_active_user(
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    if current_user.estado != "activo":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")
    return current_user


def _nombre_rol(db: Session, usuario: Usuario) -> str:
    rol = rol_service.get_rol(db, usuario.id_rol)
    return rol.nombre if rol else ""


def require_roles(*roles: str):
    """Exige que el nombre del rol del usuario esté en la lista permitida."""

    def dependency(
        current_user: Usuario = Depends(get_current_active_user),
        db: Session = Depends(get_db),
    ) -> Usuario:
        nombre = _nombre_rol(db, current_user)
        if nombre not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para esta operación",
            )
        return current_user

    return dependency


require_admin = require_roles("administrador")
require_vigilante = require_roles("vigilante")
require_admin_o_vigilante = require_roles("administrador", "vigilante")
require_ciclista = require_roles("ciclista")
require_autenticado = get_current_active_user
