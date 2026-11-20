"""Endpoints del recurso ingresos (sin DELETE/PUT — RN-009)."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import get_current_active_user, require_admin_o_vigilante
from app.dependencies.database_dependency import get_db
from app.models.usuario_model import Usuario
from app.schemas.ingreso_schema import EstadoIngreso, IngresoCreate, IngresoResponse
from app.schemas.salida_schema import SalidaCreate, SalidaResponse
from app.services import ingreso_service, salida_service

router = APIRouter(prefix="/ingresos", tags=["ingresos"])


@router.get("", response_model=list[IngresoResponse], response_model_by_alias=True)
def listar_ingresos(
    estado: EstadoIngreso | None = None,
    idBicicleta: int | None = None,
    idVigilante: int | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin_o_vigilante),
):
    return ingreso_service.list_ingresos(
        db,
        estado=estado,
        id_bicicleta=idBicicleta,
        id_vigilante=idVigilante,
    )


@router.get("/{idIngreso}", response_model=IngresoResponse, response_model_by_alias=True)
def obtener_ingreso(
    idIngreso: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
):
    return ingreso_service.get_ingreso_or_404(db, idIngreso)


@router.post(
    "",
    response_model=IngresoResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_ingreso(
    data: IngresoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin_o_vigilante),
):
    data = data.model_copy(update={"id_vigilante": current_user.id_usuario})
    return ingreso_service.create_ingreso(db, data)


@router.patch(
    "/{idIngreso}/salida",
    response_model=SalidaResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def registrar_salida_desde_ingreso(
    idIngreso: int,
    data: SalidaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin_o_vigilante),
):
    payload = data.model_dump()
    payload["id_ingreso"] = idIngreso
    payload["id_vigilante"] = current_user.id_usuario
    return salida_service.create_salida(db, SalidaCreate.model_validate(payload))
