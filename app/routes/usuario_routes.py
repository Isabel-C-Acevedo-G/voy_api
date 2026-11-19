"""Endpoints del recurso usuarios."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.usuario_schema import EstadoUsuario, UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.services import usuario_service

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("", response_model=list[UsuarioResponse], response_model_by_alias=True)
def listar_usuarios(
    estado: EstadoUsuario | None = None,
    idRol: int | None = None,
    db: Session = Depends(get_db),
):
    return usuario_service.list_usuarios(db, estado=estado, id_rol=idRol)


@router.get("/{idUsuario}", response_model=UsuarioResponse, response_model_by_alias=True)
def obtener_usuario(idUsuario: int, db: Session = Depends(get_db)):
    return usuario_service.get_usuario_or_404(db, idUsuario)


@router.post(
    "",
    response_model=UsuarioResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_service.create_usuario(db, data)


@router.patch("/{idUsuario}", response_model=UsuarioResponse, response_model_by_alias=True)
def actualizar_usuario(
    idUsuario: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
):
    return usuario_service.update_usuario(db, idUsuario, data)
