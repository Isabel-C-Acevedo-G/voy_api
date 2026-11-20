"""Endpoints del recurso espacios."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import get_current_active_user, require_admin
from app.dependencies.database_dependency import get_db
from app.models.usuario_model import Usuario
from app.schemas.espacio_schema import EspacioCreate, EspacioResponse, EspacioUpdate, EstadoEspacio
from app.services import espacio_service

router = APIRouter(prefix="/espacios", tags=["espacios"])


@router.get("", response_model=list[EspacioResponse], response_model_by_alias=True)
def listar_espacios(
    estado: EstadoEspacio | None = None,
    activo: bool | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    return espacio_service.list_espacios(db, estado=estado, activo=activo)


@router.get("/{idEspacio}", response_model=EspacioResponse, response_model_by_alias=True)
def obtener_espacio(
    idEspacio: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    return espacio_service.get_espacio_or_404(db, idEspacio)


@router.post(
    "",
    response_model=EspacioResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_espacio(
    data: EspacioCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return espacio_service.create_espacio(db, data)


@router.patch("/{idEspacio}", response_model=EspacioResponse, response_model_by_alias=True)
def actualizar_espacio(
    idEspacio: int,
    data: EspacioUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return espacio_service.update_espacio(db, idEspacio, data)
