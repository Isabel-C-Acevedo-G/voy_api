"""Endpoints del recurso usuarios."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import get_current_active_user, require_admin
from app.dependencies.database_dependency import get_db
from app.models.usuario_model import Usuario
from app.schemas.auditoria_schema import UsuarioAdminUpdate
from app.schemas.usuario_schema import EstadoUsuario, UsuarioResponse, UsuarioUpdate
from app.services import rol_service, usuario_service  # create_usuario queda solo para uso interno/legacy

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def _es_admin(db: Session, user: Usuario) -> bool:
    rol = rol_service.get_rol(db, user.id_rol)
    return bool(rol and rol.nombre == "administrador")


@router.get("", response_model=list[UsuarioResponse], response_model_by_alias=True)
def listar_usuarios(
    estado: EstadoUsuario | None = None,
    idRol: int | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return usuario_service.list_usuarios(db, estado=estado, id_rol=idRol)


@router.get("/{idUsuario}", response_model=UsuarioResponse, response_model_by_alias=True)
def obtener_usuario(
    idUsuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    if current_user.id_usuario != idUsuario and not _es_admin(db, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
    return usuario_service.get_usuario_or_404(db, idUsuario)


# Alta de usuarios: usar POST /auth/register (hashea clave). No hay POST /usuarios.


@router.patch("/{idUsuario}", response_model=UsuarioResponse, response_model_by_alias=True)
def actualizar_usuario(
    idUsuario: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user),
):
    if current_user.id_usuario != idUsuario and not _es_admin(db, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")
    return usuario_service.update_usuario(db, idUsuario, data)


@router.patch(
    "/{idUsuario}/gestion",
    response_model=UsuarioResponse,
    response_model_by_alias=True,
)
def gestionar_usuario_admin(
    idUsuario: int,
    data: UsuarioAdminUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    data = data.model_copy(update={"id_administrador": current_user.id_usuario})
    return usuario_service.admin_cambiar_usuario(db, idUsuario, data)
