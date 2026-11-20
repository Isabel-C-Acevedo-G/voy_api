"""Lógica de negocio de salidas (RF-005, RN-003, RN-007, RN-009)."""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.espacio_model import Espacio
from app.models.salida_model import Salida
from app.schemas.espacio_schema import EstadoEspacio
from app.schemas.ingreso_schema import EstadoIngreso
from app.schemas.salida_schema import SalidaCreate
from app.services import ingreso_service, usuario_service


def list_salidas(db: Session) -> list[Salida]:
    return db.query(Salida).order_by(Salida.id_salida).all()


def get_salida(db: Session, id_salida: int) -> Salida | None:
    return db.query(Salida).filter(Salida.id_salida == id_salida).first()


def get_salida_or_404(db: Session, id_salida: int) -> Salida:
    salida = get_salida(db, id_salida)
    if salida is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salida no encontrada",
        )
    return salida


def create_salida(db: Session, data: SalidaCreate) -> Salida:
    ingreso = ingreso_service.get_ingreso_or_404(db, data.id_ingreso)
    usuario_service.get_usuario_or_404(db, data.id_vigilante)

    if ingreso.estado != EstadoIngreso.activo.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El ingreso no está activo (RN-003)",
        )

    existente = db.query(Salida).filter(Salida.id_ingreso == data.id_ingreso).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una salida para este ingreso",
        )

    ahora = datetime.now(timezone.utc)
    fecha_ingreso = ingreso.fecha_ingreso
    if fecha_ingreso.tzinfo is None:
        fecha_ingreso = fecha_ingreso.replace(tzinfo=timezone.utc)
    duracion = int((ahora - fecha_ingreso).total_seconds() // 60)

    salida = Salida(
        id_ingreso=data.id_ingreso,
        fecha_salida=ahora,
        id_vigilante=data.id_vigilante,
        verificacion_marca=data.verificacion_marca,
        verificacion_color=data.verificacion_color,
        verificacion_serie=data.verificacion_serie,
        duracion_minutos=duracion,
        nota=data.nota,
        creado_en=ahora,
    )

    ingreso.estado = EstadoIngreso.cerrado.value
    espacio = db.query(Espacio).filter(Espacio.id_espacio == ingreso.id_espacio).first()
    if espacio:
        espacio.estado = EstadoEspacio.libre.value
        espacio.actualizado_en = ahora

    db.add(salida)
    db.commit()
    db.refresh(salida)
    return salida
