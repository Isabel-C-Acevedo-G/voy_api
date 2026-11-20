"""Lógica de negocio de autenticación."""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.rol_model import Rol
from app.models.usuario_model import Usuario
from app.schemas.auth_schema import TokenResponse, UsuarioRegister
from app.services import rol_service


def _rol_nombre(db: Session, id_rol: int) -> str:
    rol = rol_service.get_rol(db, id_rol)
    return rol.nombre if rol else "desconocido"


def register_usuario(db: Session, data: UsuarioRegister) -> Usuario:
    if db.query(Usuario).filter(Usuario.correo == str(data.correo)).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Correo ya registrado")
    if db.query(Usuario).filter(Usuario.documento == data.documento).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Documento ya registrado")

    id_rol = data.id_rol
    if id_rol is None:
        ciclista = db.query(Rol).filter(Rol.nombre == "ciclista").first()
        if ciclista is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No existe el rol ciclista; créalo antes de registrarte",
            )
        id_rol = ciclista.id_rol
    elif rol_service.get_rol(db, id_rol) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="idRol no existe")

    usuario = Usuario(
        nombre=data.nombre,
        tipo_documento=data.tipo_documento.value,
        documento=data.documento,
        correo=str(data.correo),
        telefono=data.telefono,
        clave_hash=get_password_hash(data.clave),
        id_rol=id_rol,
        estado="activo",
        acepta_tratamiento_datos=data.acepta_tratamiento_datos,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def authenticate_usuario(db: Session, username: str, password: str) -> Usuario:
    """username = correo o documento."""
    usuario = (
        db.query(Usuario)
        .filter((Usuario.correo == username) | (Usuario.documento == username))
        .first()
    )
    if usuario is None or not verify_password(password, usuario.clave_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if usuario.estado != "activo":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")
    return usuario


def build_token_response(db: Session, usuario: Usuario) -> TokenResponse:
    rol = _rol_nombre(db, usuario.id_rol)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": usuario.correo, "rol": rol, "uid": usuario.id_usuario})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        rol=rol,
        expira_en=expire,
    )
