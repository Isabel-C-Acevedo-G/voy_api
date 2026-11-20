"""Endpoints del recurso incidentes."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import require_admin_o_vigilante
from app.dependencies.database_dependency import get_db
from app.models.usuario_model import Usuario
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
    _: Usuario = Depends(require_admin_o_vigilante),
):
    return incidente_service.list_incidentes(db, estado=estado, tipo=tipo)


@router.get("/{idIncidente}", response_model=IncidenteResponse, response_model_by_alias=True)
def obtener_incidente(
    idIncidente: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin_o_vigilante),
):
    return incidente_service.get_incidente_or_404(db, idIncidente)


@router.post(
    "",
    response_model=IncidenteResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_incidente(
    data: IncidenteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin_o_vigilante),
):
    data = data.model_copy(update={"id_responsable": current_user.id_usuario})
    return incidente_service.create_incidente(db, data)


@router.patch("/{idIncidente}", response_model=IncidenteResponse, response_model_by_alias=True)
def actualizar_incidente(
    idIncidente: int,
    data: IncidenteUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin_o_vigilante),
):
    return incidente_service.update_incidente(db, idIncidente, data)
