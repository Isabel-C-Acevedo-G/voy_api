"""Endpoints del recurso ingresos (sin DELETE/PUT — RN-009)."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.ingreso_schema import EstadoIngreso, IngresoCreate, IngresoResponse
from app.services import ingreso_service

router = APIRouter(prefix="/ingresos", tags=["ingresos"])


@router.post(
    "",
    response_model=IngresoResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_ingreso(data: IngresoCreate, db: Session = Depends(get_db)):
    return ingreso_service.create_ingreso(db, data)
