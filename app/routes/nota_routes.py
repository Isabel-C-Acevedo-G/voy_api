"""Endpoints del recurso notas."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import require_admin, require_admin_o_vigilante
from app.dependencies.database_dependency import get_db
from app.models.usuario_model import Usuario
from app.schemas.nota_schema import NotaCreate, NotaResponse, TipoMovimiento
from app.services import nota_service

router = APIRouter(prefix="/notas", tags=["notas"])


@router.get("", response_model=list[NotaResponse], response_model_by_alias=True)
def listar_notas(
    tipoMovimiento: TipoMovimiento | None = None,
    idMovimiento: int | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin_o_vigilante),
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
def crear_nota(
    data: NotaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    data = data.model_copy(update={"id_administrador": current_user.id_usuario})
    return nota_service.create_nota(db, data)
