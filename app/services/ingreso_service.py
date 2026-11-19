"""Lógica de negocio de ingresos (RF-004, RN-003, RN-004, RN-009)."""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.espacio_model import Espacio
from app.models.ingreso_model import Ingreso
from app.schemas.espacio_schema import EstadoEspacio
from app.schemas.ingreso_schema import EstadoIngreso, IngresoCreate
from app.services import bicicleta_service, usuario_service


def list_ingresos(
    db: Session,
    estado: EstadoIngreso | None = None,
    id_bicicleta: int | None = None,
    id_vigilante: int | None = None,
) -> list[Ingreso]:
    query = db.query(Ingreso)
    if estado is not None:
        query = query.filter(Ingreso.estado == estado.value)
    if id_bicicleta is not None:
        query = query.filter(Ingreso.id_bicicleta == id_bicicleta)
    if id_vigilante is not None:
        query = query.filter(Ingreso.id_vigilante == id_vigilante)
    return query.order_by(Ingreso.id_ingreso).all()


def get_ingreso(db: Session, id_ingreso: int) -> Ingreso | None:
    return db.query(Ingreso).filter(Ingreso.id_ingreso == id_ingreso).first()


def get_ingreso_or_404(db: Session, id_ingreso: int) -> Ingreso:
    ingreso = get_ingreso(db, id_ingreso)
    if ingreso is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingreso no encontrado",
        )
    return ingreso


def _asignar_espacio_libre(db: Session) -> Espacio:
    """RN-004: el sistema elige un espacio libre y activo."""
    espacio = (
        db.query(Espacio)
        .filter(
            Espacio.estado == EstadoEspacio.libre.value,
            Espacio.activo.is_(True),
        )
        .order_by(Espacio.id_espacio)
        .first()
    )
    if espacio is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No hay espacios libres disponibles",
        )
    return espacio


def create_ingreso(db: Session, data: IngresoCreate) -> Ingreso:
    bicicleta = bicicleta_service.get_bicicleta_or_404(db, data.id_bicicleta)
    if bicicleta.estado != "activa":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La bicicleta no está activa",
        )

    usuario_service.get_usuario_or_404(db, data.id_vigilante)

    activo = (
        db.query(Ingreso)
        .filter(
            Ingreso.id_bicicleta == data.id_bicicleta,
            Ingreso.estado == EstadoIngreso.activo.value,
        )
        .first()
    )
    if activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La bicicleta ya tiene un ingreso activo",
        )

    espacio = _asignar_espacio_libre(db)
    ahora = datetime.now(timezone.utc)

    ingreso = Ingreso(
        id_bicicleta=data.id_bicicleta,
        id_espacio=espacio.id_espacio,
        id_reserva=data.id_reserva,
        fecha_ingreso=ahora,
        id_vigilante=data.id_vigilante,
        observaciones=data.observaciones or "",
        estado=EstadoIngreso.activo.value,
        creado_en=ahora,
    )
    espacio.estado = EstadoEspacio.ocupado.value
    espacio.actualizado_en = ahora

    db.add(ingreso)
    db.commit()
    db.refresh(ingreso)
    return ingreso
