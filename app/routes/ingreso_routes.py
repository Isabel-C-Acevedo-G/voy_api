"""Endpoints del recurso ingresos (sin DELETE/PUT — RN-009)."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.ingreso_schema import EstadoIngreso, IngresoCreate, IngresoResponse
from app.services import ingreso_service

router = APIRouter(prefix="/ingresos", tags=["ingresos"])


@router.get("", response_model=list[IngresoResponse], response_model_by_alias=True)
def listar_ingresos(
    estado: EstadoIngreso | None = None,
    idBicicleta: int | None = None,
    idVigilante: int | None = None,
    db: Session = Depends(get_db),
):
    return ingreso_service.list_ingresos(
        db,
        estado=estado,
        id_bicicleta=idBicicleta,
        id_vigilante=idVigilante,
    )


@router.get("/{idIngreso}", response_model=IngresoResponse, response_model_by_alias=True)
def obtener_ingreso(idIngreso: int, db: Session = Depends(get_db)):
    return ingreso_service.get_ingreso_or_404(db, idIngreso)


@router.post(
    "",
    response_model=IngresoResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_ingreso(data: IngresoCreate, db: Session = Depends(get_db)):
    return ingreso_service.create_ingreso(db, data)
