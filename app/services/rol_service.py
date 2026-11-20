"""Lógica de negocio del recurso roles."""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.rol_model import Rol
from app.schemas.rol_schema import RolCreate


def list_roles(db: Session) -> list[Rol]:
    return db.query(Rol).order_by(Rol.id_rol).all()


def get_rol(db: Session, id_rol: int) -> Rol | None:
    return db.query(Rol).filter(Rol.id_rol == id_rol).first()


def create_rol(db: Session, data: RolCreate) -> Rol:
    existente = db.query(Rol).filter(Rol.nombre == data.nombre).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un rol con ese nombre",
        )
    rol = Rol(nombre=data.nombre)
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol
