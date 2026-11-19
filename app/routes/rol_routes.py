"""Endpoints del recurso roles."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.rol_schema import RolCreate, RolResponse
from app.services import rol_service

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=list[RolResponse], response_model_by_alias=True)
def listar_roles(db: Session = Depends(get_db)):
    return rol_service.list_roles(db)


@router.post(
    "",
    response_model=RolResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
def crear_rol(data: RolCreate, db: Session = Depends(get_db)):
    return rol_service.create_rol(db, data)
