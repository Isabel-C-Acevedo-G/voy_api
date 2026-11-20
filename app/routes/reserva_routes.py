"""Endpoints del recurso reservas."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import get_current_active_user
from app.dependencies.database_dependency import get_db
from app.models.usuario_model import Usuario
from app.schemas.reserva_schema import EstadoReserva, ReservaCreate, ReservaResponse
from app.services import reserva_service

router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.get("", response_model=list[ReservaResponse], response_model_by_alias=True)
def listar_reservas(
    estado: EstadoReserva | None = None,
    idUsuario: int | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    return reserva_service.list_reservas(db, estado=estado, id_usuario=idUsuario)


@router.get("/{idReserva}", response_model=ReservaResponse, response_model_by_alias=True)
def obtener_reserva(
    idReserva: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    return reserva_service.get_reserva_or_404(db, idReserva)


@router.post(
    "",
    response_model=ReservaResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_reserva(
    data: ReservaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    data = data.model_copy(update={"id_usuario": current_user.id_usuario})
    return reserva_service.create_reserva(db, data)


@router.patch(
    "/{idReserva}/cancelar",
    response_model=ReservaResponse,
    response_model_by_alias=True,
)
def cancelar_reserva(
    idReserva: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    return reserva_service.cancelar_reserva(db, idReserva)
