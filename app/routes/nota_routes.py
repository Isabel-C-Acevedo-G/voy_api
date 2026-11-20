"""Endpoints del recurso notas."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.nota_schema import NotaCreate, NotaResponse, TipoMovimiento
from app.services import nota_service

router = APIRouter(prefix="/notas", tags=["notas"])


@router.get("", response_model=list[NotaResponse], response_model_by_alias=True)
def listar_notas(
    tipoMovimiento: TipoMovimiento | None = None,
    idMovimiento: int | None = None,
    db: Session = Depends(get_db),
):
    return nota_service.list_notas(
        db,
        tipo_movimiento=tipoMovimiento,
        id_movimiento=idMovimiento,
    )


@router.post(
    "",
    response_model=NotaResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_nota(data: NotaCreate, db: Session = Depends(get_db)):
    return nota_service.create_nota(db, data)
