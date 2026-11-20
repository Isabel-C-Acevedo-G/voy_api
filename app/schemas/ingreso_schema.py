"""Esquemas Pydantic para ingresos (RF-004)."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class EstadoIngreso(str, Enum):
    activo = "activo"
    cerrado = "cerrado"


class IngresoCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_bicicleta: int = Field(..., alias="idBicicleta")
    id_vigilante: int = Field(..., alias="idVigilante")  # hasta Fase 7 (JWT)
    id_reserva: int | None = Field(default=None, alias="idReserva")
    observaciones: str | None = Field(default=None, max_length=200)


class IngresoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id_ingreso: int = Field(serialization_alias="idIngreso")
    id_bicicleta: int = Field(serialization_alias="idBicicleta")
    id_espacio: int = Field(serialization_alias="idEspacio")
    id_reserva: int | None = Field(default=None, serialization_alias="idReserva")
    fecha_ingreso: datetime = Field(serialization_alias="fechaIngreso")
    id_vigilante: int = Field(serialization_alias="idVigilante")
    observaciones: str | None = None
    estado: EstadoIngreso
    creado_en: datetime = Field(serialization_alias="creadoEn")
