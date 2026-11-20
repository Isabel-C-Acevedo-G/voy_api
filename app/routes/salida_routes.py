"""Endpoints del recurso salidas (sin DELETE/PUT — RN-009)."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.salida_schema import SalidaCreate, SalidaResponse
from app.services import salida_service

router = APIRouter(prefix="/salidas", tags=["salidas"])


@router.get("", response_model=list[SalidaResponse], response_model_by_alias=True)
def listar_salidas(db: Session = Depends(get_db)):
    return salida_service.list_salidas(db)


@router.get("/{idSalida}", response_model=SalidaResponse, response_model_by_alias=True)
def obtener_salida(idSalida: int, db: Session = Depends(get_db)):
    return salida_service.get_salida_or_404(db, idSalida)


@router.post(
    "",
    response_model=SalidaResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_salida(data: SalidaCreate, db: Session = Depends(get_db)):
    return salida_service.create_salida(db, data)
