"""Esquemas Pydantic para reservas (RF-007)."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class EstadoReserva(str, Enum):
    activa = "activa"
    usada = "usada"
    cancelada = "cancelada"
    vencida = "vencida"


class ReservaCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_espacio: int = Field(..., alias="idEspacio")
    id_usuario: int = Field(..., alias="idUsuario")  # hasta Fase 7 (JWT)


class ReservaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id_reserva: int = Field(serialization_alias="idReserva")
    id_usuario: int = Field(serialization_alias="idUsuario")
    id_espacio: int = Field(serialization_alias="idEspacio")
    fecha_reserva: datetime = Field(serialization_alias="fechaReserva")
    fecha_expiracion: datetime = Field(serialization_alias="fechaExpiracion")
    estado: EstadoReserva
    creado_en: datetime = Field(serialization_alias="creadoEn")
