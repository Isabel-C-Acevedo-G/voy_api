"""Esquemas Pydantic para espacios del parqueadero."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class EstadoEspacio(str, Enum):
    libre = "libre"
    ocupado = "ocupado"
    reservado = "reservado"


class EspacioCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    codigo: str = Field(..., min_length=1, max_length=20, examples=["A-01"])
    activo: bool = True


class EspacioUpdate(BaseModel):
    """Solo código / activo. El estado lo cambian ingresos/salidas/reservas."""

    model_config = ConfigDict(populate_by_name=True)

    codigo: str | None = Field(default=None, min_length=1, max_length=20)
    activo: bool | None = None


class EspacioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id_espacio: int = Field(serialization_alias="idEspacio")
    codigo: str
    estado: EstadoEspacio
    activo: bool
    creado_en: datetime = Field(serialization_alias="creadoEn")
    actualizado_en: datetime | None = Field(default=None, serialization_alias="actualizadoEn")
