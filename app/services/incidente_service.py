"""Lógica de negocio de incidentes (RF-008)."""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.incidente_model import Incidente
from app.schemas.incidente_schema import EstadoIncidente, IncidenteCreate, IncidenteUpdate, TipoIncidente
from app.services import bicicleta_service, usuario_service


def list_incidentes(
    db: Session,
    estado: EstadoIncidente | None = None,
    tipo: TipoIncidente | None = None,
) -> list[Incidente]:
    query = db.query(Incidente)
    if estado is not None:
        query = query.filter(Incidente.estado == estado.value)
    if tipo is not None:
        query = query.filter(Incidente.tipo == tipo.value)
    return query.order_by(Incidente.id_incidente).all()


def get_incidente_or_404(db: Session, id_incidente: int) -> Incidente:
    incidente = db.query(Incidente).filter(Incidente.id_incidente == id_incidente).first()
    if incidente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incidente no encontrado")
    return incidente


def create_incidente(db: Session, data: IncidenteCreate) -> Incidente:
    usuario_service.get_usuario_or_404(db, data.id_responsable)
    if data.id_bicicleta is not None:
        bicicleta_service.get_bicicleta_or_404(db, data.id_bicicleta)
    if data.id_usuario_involucrado is not None:
        usuario_service.get_usuario_or_404(db, data.id_usuario_involucrado)

    ahora = datetime.now(timezone.utc)
    incidente = Incidente(
        tipo=data.tipo.value,
        descripcion=data.descripcion,
        fecha=ahora,
        id_bicicleta=data.id_bicicleta,
        id_usuario_involucrado=data.id_usuario_involucrado,
        foto=data.foto,
        id_responsable=data.id_responsable,
        estado=EstadoIncidente.abierto.value,
        creado_en=ahora,
    )
    db.add(incidente)
    db.commit()
    db.refresh(incidente)
    return incidente


def update_incidente(db: Session, id_incidente: int, data: IncidenteUpdate) -> Incidente:
    incidente = get_incidente_or_404(db, id_incidente)
    cambios = data.model_dump(exclude_unset=True)
    if "estado" in cambios and cambios["estado"] is not None:
        cambios["estado"] = cambios["estado"].value
    for campo, valor in cambios.items():
        setattr(incidente, campo, valor)
    db.commit()
    db.refresh(incidente)
    return incidente
