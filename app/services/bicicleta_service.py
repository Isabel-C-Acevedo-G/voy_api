"""Lógica de negocio del recurso bicicletas (RF-003, RN-001, RN-002)."""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.bicicleta_model import Bicicleta
from app.schemas.bicicleta_schema import (
    BicicletaCreate,
    BicicletaEstadoUpdate,
    BicicletaUpdate,
    EstadoBicicleta,
)
from app.services import usuario_service


def list_bicicletas(
    db: Session,
    id_propietario: int | None = None,
    estado: EstadoBicicleta | None = None,
    numero_serie: str | None = None,
) -> list[Bicicleta]:
    query = db.query(Bicicleta)
    if id_propietario is not None:
        query = query.filter(Bicicleta.id_propietario == id_propietario)
    if estado is not None:
        query = query.filter(Bicicleta.estado == estado.value)
    if numero_serie is not None:
        query = query.filter(Bicicleta.numero_serie == numero_serie)
    return query.order_by(Bicicleta.id_bicicleta).all()


def get_bicicleta(db: Session, id_bicicleta: int) -> Bicicleta | None:
    return db.query(Bicicleta).filter(Bicicleta.id_bicicleta == id_bicicleta).first()


def get_bicicleta_or_404(db: Session, id_bicicleta: int) -> Bicicleta:
    bicicleta = get_bicicleta(db, id_bicicleta)
    if bicicleta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bicicleta no encontrada",
        )
    return bicicleta


def create_bicicleta(db: Session, data: BicicletaCreate) -> Bicicleta:
    # RN-002: propietario debe existir
    usuario_service.get_usuario_or_404(db, data.id_propietario)

    # RN-001: numeroSerie único
    if db.query(Bicicleta).filter(Bicicleta.numero_serie == data.numero_serie).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una bicicleta con ese numeroSerie (RN-001)",
        )

    bicicleta = Bicicleta(
        id_propietario=data.id_propietario,
        marca=data.marca,
        modelo=data.modelo,
        color=data.color,
        tipo=data.tipo.value if data.tipo else None,
        numero_serie=data.numero_serie,
        foto=data.foto,
        estado=EstadoBicicleta.activa.value,
    )
    db.add(bicicleta)
    db.commit()
    db.refresh(bicicleta)
    return bicicleta


def update_bicicleta(db: Session, id_bicicleta: int, data: BicicletaUpdate) -> Bicicleta:
    bicicleta = get_bicicleta_or_404(db, id_bicicleta)
    cambios = data.model_dump(exclude_unset=True)

    if "tipo" in cambios and cambios["tipo"] is not None:
        cambios["tipo"] = cambios["tipo"].value

    for campo, valor in cambios.items():
        setattr(bicicleta, campo, valor)

    bicicleta.actualizado_en = datetime.now(timezone.utc)
    db.commit()
    db.refresh(bicicleta)
    return bicicleta


def update_estado_bicicleta(
    db: Session,
    id_bicicleta: int,
    data: BicicletaEstadoUpdate,
) -> Bicicleta:
    """Cambio de estado (RN-008). Auth de admin se aplica en Fase 7."""
    bicicleta = get_bicicleta_or_404(db, id_bicicleta)
    bicicleta.estado = data.estado.value
    bicicleta.actualizado_en = datetime.now(timezone.utc)
    db.commit()
    db.refresh(bicicleta)
    return bicicleta
