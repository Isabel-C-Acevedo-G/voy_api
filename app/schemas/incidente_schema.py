"""Esquemas Pydantic para incidentes (RF-008)."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TipoIncidente(str, Enum):
    dano = "daño"
    perdida = "pérdida"
    intento_robo = "intento de robo"
    conducta = "conducta"
    otro = "otro"


class EstadoIncidente(str, Enum):
    abierto = "abierto"
    cerrado = "cerrado"


class IncidenteCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    tipo: TipoIncidente
    descripcion: str = Field(..., min_length=1, max_length=500)
    id_bicicleta: int | None = Field(default=None, alias="idBicicleta")
    id_usuario_involucrado: int | None = Field(default=None, alias="idUsuarioInvolucrado")
    foto: str | None = Field(default=None, max_length=255)
    id_responsable: int = Field(..., alias="idResponsable")  # hasta Fase 7 (JWT)

    @field_validator("foto")
    @classmethod
    def foto_jpg_png(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        lower = value.lower()
        if not (lower.endswith(".jpg") or lower.endswith(".jpeg") or lower.endswith(".png")):
            raise ValueError("foto debe ser ruta .jpg o .png")
        return value


class IncidenteUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    descripcion: str | None = Field(default=None, min_length=1, max_length=500)
    estado: EstadoIncidente | None = None
    foto: str | None = Field(default=None, max_length=255)


class IncidenteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id_incidente: int = Field(serialization_alias="idIncidente")
    tipo: TipoIncidente
    descripcion: str
    fecha: datetime
    id_bicicleta: int | None = Field(default=None, serialization_alias="idBicicleta")
    id_usuario_involucrado: int | None = Field(default=None, serialization_alias="idUsuarioInvolucrado")
    foto: str | None = None
    id_responsable: int = Field(serialization_alias="idResponsable")
    estado: EstadoIncidente
    creado_en: datetime = Field(serialization_alias="creadoEn")
