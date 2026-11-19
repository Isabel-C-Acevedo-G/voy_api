"""Lógica de negocio del recurso espacios."""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.espacio_model import Espacio
from app.schemas.espacio_schema import EspacioCreate, EspacioUpdate, EstadoEspacio


def list_espacios(
    db: Session,
    estado: EstadoEspacio | None = None,
    activo: bool | None = None,
) -> list[Espacio]:
    query = db.query(Espacio)
    if estado is not None:
        query = query.filter(Espacio.estado == estado.value)
    if activo is not None:
        query = query.filter(Espacio.activo == activo)
    return query.order_by(Espacio.id_espacio).all()


def get_espacio(db: Session, id_espacio: int) -> Espacio | None:
    return db.query(Espacio).filter(Espacio.id_espacio == id_espacio).first()


def get_espacio_or_404(db: Session, id_espacio: int) -> Espacio:
    espacio = get_espacio(db, id_espacio)
    if espacio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Espacio no encontrado",
        )
    return espacio


def create_espacio(db: Session, data: EspacioCreate) -> Espacio:
    if db.query(Espacio).filter(Espacio.codigo == data.codigo).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un espacio con ese código",
        )
    espacio = Espacio(
        codigo=data.codigo,
        estado=EstadoEspacio.libre.value,
        activo=data.activo,
    )
    db.add(espacio)
    db.commit()
    db.refresh(espacio)
    return espacio


def update_espacio(db: Session, id_espacio: int, data: EspacioUpdate) -> Espacio:
    espacio = get_espacio_or_404(db, id_espacio)
    cambios = data.model_dump(exclude_unset=True)

    if "codigo" in cambios and cambios["codigo"] is not None:
        otro = (
            db.query(Espacio)
            .filter(Espacio.codigo == cambios["codigo"], Espacio.id_espacio != id_espacio)
            .first()
        )
        if otro:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un espacio con ese código",
            )

    for campo, valor in cambios.items():
        setattr(espacio, campo, valor)

    espacio.actualizado_en = datetime.now(timezone.utc)
    db.commit()
    db.refresh(espacio)
    return espacio
