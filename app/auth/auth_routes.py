"""Endpoints de autenticación."""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import auth_service
from app.dependencies.auth_dependency import get_current_active_user
from app.dependencies.database_dependency import get_db
from app.models.usuario_model import Usuario
from app.schemas.auth_schema import TokenResponse, UsuarioRegister
from app.schemas.usuario_schema import UsuarioResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UsuarioResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def register(data: UsuarioRegister, db: Session = Depends(get_db)):
    return auth_service.register_usuario(db, data)


@router.post("/login", response_model=TokenResponse, response_model_by_alias=True)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """OAuth2: username = correo o documento, password = clave."""
    usuario = auth_service.authenticate_usuario(db, form_data.username, form_data.password)
    return auth_service.build_token_response(db, usuario)


@router.get("/me", response_model=UsuarioResponse, response_model_by_alias=True)
def me(current_user: Usuario = Depends(get_current_active_user)):
    return current_user
