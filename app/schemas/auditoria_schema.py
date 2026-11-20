"""Esquemas para cambio de estado/rol con auditoría (RF-009)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.usuario_schema import EstadoUsuario, UsuarioResponse


class UsuarioAdminUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nuevo_estado: EstadoUsuario | None = Field(default=None, alias="nuevoEstado")
    nuevo_rol: int | None = Field(default=None, alias="nuevoRol")
    motivo: str = Field(..., min_length=1, max_length=200)
    id_administrador: int = Field(..., alias="idAdministrador")  # hasta Fase 7


class AuditoriaUsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id_auditoria: int = Field(serialization_alias="idAuditoria")
    id_usuario: int = Field(serialization_alias="idUsuario")
    nuevo_estado: str | None = Field(default=None, serialization_alias="nuevoEstado")
    nuevo_rol: int | None = Field(default=None, serialization_alias="nuevoRol")
    id_administrador: int = Field(serialization_alias="idAdministrador")
    fecha_cambio: datetime = Field(serialization_alias="fechaCambio")
    motivo: str
    usuario: UsuarioResponse | None = None
