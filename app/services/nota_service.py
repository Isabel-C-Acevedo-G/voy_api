"""Lógica de negocio de notas (RN-009)."""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.nota_model import Nota
from app.schemas.nota_schema import NotaCreate, TipoMovimiento
from app.services import ingreso_service, salida_service, usuario_service


def list_notas(
    db: Session,
    tipo_movimiento: TipoMovimiento | None = None,
    id_movimiento: int | None = None,
) -> list[Nota]:
    query = db.query(Nota)
    if tipo_movimiento is not None:
        query = query.filter(Nota.tipo_movimiento == tipo_movimiento.value)
    if id_movimiento is not None:
        query = query.filter(Nota.id_movimiento == id_movimiento)
    return query.order_by(Nota.id_nota).all()


def create_nota(db: Session, data: NotaCreate) -> Nota:
    usuario_service.get_usuario_or_404(db, data.id_administrador)

    if data.tipo_movimiento == TipoMovimiento.ingreso:
        ingreso_service.get_ingreso_or_404(db, data.id_movimiento)
    else:
        salida_service.get_salida_or_404(db, data.id_movimiento)

    nota = Nota(
        tipo_movimiento=data.tipo_movimiento.value,
        id_movimiento=data.id_movimiento,
        texto=data.texto,
        id_administrador=data.id_administrador,
        fecha=datetime.now(timezone.utc),
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    return nota
