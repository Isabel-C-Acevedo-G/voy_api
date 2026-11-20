"""Lógica de negocio de reservas (RF-007, RN-005)."""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.espacio_model import Espacio
from app.models.reserva_model import Reserva
from app.schemas.espacio_schema import EstadoEspacio
from app.schemas.reserva_schema import EstadoReserva, ReservaCreate
from app.services import usuario_service

RESERVA_MINUTOS = 30


def _aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def vencer_reservas_caducadas(db: Session) -> int:
    """Marca como vencidas las activas cuya fechaExpiracion ya pasó y libera el espacio."""
    ahora = datetime.now(timezone.utc)
    activas = db.query(Reserva).filter(Reserva.estado == EstadoReserva.activa.value).all()
    cambiadas = 0
    for reserva in activas:
        if _aware(reserva.fecha_expiracion) <= ahora:
            reserva.estado = EstadoReserva.vencida.value
            espacio = db.query(Espacio).filter(Espacio.id_espacio == reserva.id_espacio).first()
            if espacio and espacio.estado == EstadoEspacio.reservado.value:
                espacio.estado = EstadoEspacio.libre.value
                espacio.actualizado_en = ahora
            cambiadas += 1
    if cambiadas:
        db.commit()
    return cambiadas


def list_reservas(
    db: Session,
    estado: EstadoReserva | None = None,
    id_usuario: int | None = None,
) -> list[Reserva]:
    vencer_reservas_caducadas(db)
    query = db.query(Reserva)
    if estado is not None:
        query = query.filter(Reserva.estado == estado.value)
    if id_usuario is not None:
        query = query.filter(Reserva.id_usuario == id_usuario)
    return query.order_by(Reserva.id_reserva).all()


def get_reserva(db: Session, id_reserva: int) -> Reserva | None:
    vencer_reservas_caducadas(db)
    return db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()


def get_reserva_or_404(db: Session, id_reserva: int) -> Reserva:
    reserva = get_reserva(db, id_reserva)
    if reserva is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada",
        )
    return reserva


def create_reserva(db: Session, data: ReservaCreate) -> Reserva:
    vencer_reservas_caducadas(db)
    usuario_service.get_usuario_or_404(db, data.id_usuario)

    activa = (
        db.query(Reserva)
        .filter(
            Reserva.id_usuario == data.id_usuario,
            Reserva.estado == EstadoReserva.activa.value,
        )
        .first()
    )
    if activa:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya tiene una reserva activa",
        )

    espacio = db.query(Espacio).filter(Espacio.id_espacio == data.id_espacio).first()
    if espacio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Espacio no encontrado")
    if not espacio.activo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El espacio no está activo")
    if espacio.estado != EstadoEspacio.libre.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El espacio no está libre",
        )

    ahora = datetime.now(timezone.utc)
    reserva = Reserva(
        id_usuario=data.id_usuario,
        id_espacio=data.id_espacio,
        fecha_reserva=ahora,
        fecha_expiracion=ahora + timedelta(minutes=RESERVA_MINUTOS),
        estado=EstadoReserva.activa.value,
        creado_en=ahora,
    )
    espacio.estado = EstadoEspacio.reservado.value
    espacio.actualizado_en = ahora

    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva


def cancelar_reserva(db: Session, id_reserva: int) -> Reserva:
    reserva = get_reserva_or_404(db, id_reserva)
    if reserva.estado != EstadoReserva.activa.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Solo se puede cancelar una reserva activa",
        )

    ahora = datetime.now(timezone.utc)
    reserva.estado = EstadoReserva.cancelada.value
    espacio = db.query(Espacio).filter(Espacio.id_espacio == reserva.id_espacio).first()
    if espacio and espacio.estado == EstadoEspacio.reservado.value:
        espacio.estado = EstadoEspacio.libre.value
        espacio.actualizado_en = ahora

    db.commit()
    db.refresh(reserva)
    return reserva
