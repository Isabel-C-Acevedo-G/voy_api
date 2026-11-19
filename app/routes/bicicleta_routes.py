"""Endpoints del recurso bicicletas."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.bicicleta_schema import (
    BicicletaCreate,
    BicicletaEstadoUpdate,
    BicicletaResponse,
    BicicletaUpdate,
    EstadoBicicleta,
)
from app.services import bicicleta_service

router = APIRouter(prefix="/bicicletas", tags=["bicicletas"])


@router.get("", response_model=list[BicicletaResponse], response_model_by_alias=True)
def listar_bicicletas(
    idPropietario: int | None = None,
    estado: EstadoBicicleta | None = None,
    numeroSerie: str | None = None,
    db: Session = Depends(get_db),
):
    return bicicleta_service.list_bicicletas(
        db,
        id_propietario=idPropietario,
        estado=estado,
        numero_serie=numeroSerie,
    )


@router.get("/{idBicicleta}", response_model=BicicletaResponse, response_model_by_alias=True)
def obtener_bicicleta(idBicicleta: int, db: Session = Depends(get_db)):
    return bicicleta_service.get_bicicleta_or_404(db, idBicicleta)


@router.post(
    "",
    response_model=BicicletaResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_bicicleta(data: BicicletaCreate, db: Session = Depends(get_db)):
    return bicicleta_service.create_bicicleta(db, data)


@router.patch("/{idBicicleta}", response_model=BicicletaResponse, response_model_by_alias=True)
def actualizar_bicicleta(
    idBicicleta: int,
    data: BicicletaUpdate,
    db: Session = Depends(get_db),
):
    return bicicleta_service.update_bicicleta(db, idBicicleta, data)


@router.patch(
    "/{idBicicleta}/estado",
    response_model=BicicletaResponse,
    response_model_by_alias=True,
)
def cambiar_estado_bicicleta(
    idBicicleta: int,
    data: BicicletaEstadoUpdate,
    db: Session = Depends(get_db),
):
    """Activar/desactivar (RN-008). Auth admin se aplica en Fase 7."""
    return bicicleta_service.update_estado_bicicleta(db, idBicicleta, data)
