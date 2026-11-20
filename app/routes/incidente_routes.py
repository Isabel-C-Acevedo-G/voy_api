"""Endpoints del recurso incidentes."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.incidente_schema import (
    EstadoIncidente,
    IncidenteCreate,
    IncidenteResponse,
    IncidenteUpdate,
    TipoIncidente,
)
from app.services import incidente_service

router = APIRouter(prefix="/incidentes", tags=["incidentes"])


@router.get("", response_model=list[IncidenteResponse], response_model_by_alias=True)
def listar_incidentes(
    estado: EstadoIncidente | None = None,
    tipo: TipoIncidente | None = None,
    db: Session = Depends(get_db),
):
    return incidente_service.list_incidentes(db, estado=estado, tipo=tipo)


@router.get("/{idIncidente}", response_model=IncidenteResponse, response_model_by_alias=True)
def obtener_incidente(idIncidente: int, db: Session = Depends(get_db)):
    return incidente_service.get_incidente_or_404(db, idIncidente)


@router.post(
    "",
    response_model=IncidenteResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_incidente(data: IncidenteCreate, db: Session = Depends(get_db)):
    return incidente_service.create_incidente(db, data)


@router.patch("/{idIncidente}", response_model=IncidenteResponse, response_model_by_alias=True)
def actualizar_incidente(
    idIncidente: int,
    data: IncidenteUpdate,
    db: Session = Depends(get_db),
):
    return incidente_service.update_incidente(db, idIncidente, data)
