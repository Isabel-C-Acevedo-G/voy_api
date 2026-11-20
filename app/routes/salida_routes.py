"""Endpoints del recurso salidas (sin DELETE/PUT — RN-009)."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import get_current_active_user, require_admin_o_vigilante
from app.dependencies.database_dependency import get_db
from app.models.usuario_model import Usuario
from app.schemas.salida_schema import SalidaCreate, SalidaResponse
from app.services import salida_service

router = APIRouter(prefix="/salidas", tags=["salidas"])


@router.get("", response_model=list[SalidaResponse], response_model_by_alias=True)
def listar_salidas(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin_o_vigilante),
):
    return salida_service.list_salidas(db)


@router.get("/{idSalida}", response_model=SalidaResponse, response_model_by_alias=True)
def obtener_salida(
    idSalida: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    return salida_service.get_salida_or_404(db, idSalida)


@router.post(
    "",
    response_model=SalidaResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_salida(
    data: SalidaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin_o_vigilante),
):
    data = data.model_copy(update={"id_vigilante": current_user.id_usuario})
    return salida_service.create_salida(db, data)
