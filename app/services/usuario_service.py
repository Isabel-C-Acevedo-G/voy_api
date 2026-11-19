"""Lógica de negocio del recurso usuarios."""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import EstadoUsuario, UsuarioCreate, UsuarioUpdate
from app.services import rol_service


def list_usuarios(
    db: Session,
    estado: EstadoUsuario | None = None,
    id_rol: int | None = None,
) -> list[Usuario]:
    query = db.query(Usuario)
    if estado is not None:
        query = query.filter(Usuario.estado == estado.value)
    if id_rol is not None:
        query = query.filter(Usuario.id_rol == id_rol)
    return query.order_by(Usuario.id_usuario).all()


def get_usuario(db: Session, id_usuario: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def get_usuario_or_404(db: Session, id_usuario: int) -> Usuario:
    usuario = get_usuario(db, id_usuario)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return usuario


def create_usuario(db: Session, data: UsuarioCreate) -> Usuario:
    if rol_service.get_rol(db, data.id_rol) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="idRol no existe en la colección roles",
        )

    if db.query(Usuario).filter(Usuario.correo == str(data.correo)).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese correo",
        )
    if db.query(Usuario).filter(Usuario.documento == data.documento).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese documento",
        )

    usuario = Usuario(
        nombre=data.nombre,
        tipo_documento=data.tipo_documento.value,
        documento=data.documento,
        correo=str(data.correo),
        telefono=data.telefono,
        id_rol=data.id_rol,
        estado=data.estado.value,
        acepta_tratamiento_datos=data.acepta_tratamiento_datos,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def update_usuario(db: Session, id_usuario: int, data: UsuarioUpdate) -> Usuario:
    usuario = get_usuario_or_404(db, id_usuario)
    cambios = data.model_dump(exclude_unset=True)

    if "id_rol" in cambios and cambios["id_rol"] is not None:
        if rol_service.get_rol(db, cambios["id_rol"]) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="idRol no existe en la colección roles",
            )

    if "estado" in cambios and cambios["estado"] is not None:
        cambios["estado"] = cambios["estado"].value

    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)

    usuario.actualizado_en = datetime.now(timezone.utc)
    db.commit()
    db.refresh(usuario)
    return usuario
