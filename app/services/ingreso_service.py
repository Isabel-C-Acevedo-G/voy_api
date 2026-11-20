"""Lógica de negocio de ingresos (RF-004, RN-003, RN-004, RN-006, RN-009)."""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.espacio_model import Espacio
from app.models.ingreso_model import Ingreso
from app.models.reserva_model import Reserva
from app.schemas.espacio_schema import EstadoEspacio
from app.schemas.ingreso_schema import EstadoIngreso, IngresoCreate
from app.schemas.reserva_schema import EstadoReserva
from app.services import bicicleta_service, reserva_service, usuario_service


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
    reserva_service.vencer_reservas_caducadas(db)

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

    ahora = datetime.now(timezone.utc)
    reserva: Reserva | None = None

    if data.id_reserva is not None:
        # RN-006: llegada con reserva
        reserva = reserva_service.get_reserva_or_404(db, data.id_reserva)
        if reserva.estado != EstadoReserva.activa.value:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La reserva no está activa",
            )
        if reserva.id_usuario != bicicleta.id_propietario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La reserva no pertenece al propietario de la bicicleta",
            )
        espacio = db.query(Espacio).filter(Espacio.id_espacio == reserva.id_espacio).first()
        if espacio is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Espacio no encontrado")
    else:
        espacio = _asignar_espacio_libre(db)

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

    if reserva is not None:
        reserva.estado = EstadoReserva.usada.value

    db.add(ingreso)
    db.commit()
    db.refresh(ingreso)
    return ingreso
