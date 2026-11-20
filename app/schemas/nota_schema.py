"""Esquemas Pydantic para notas aclaratorias (RN-009)."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TipoMovimiento(str, Enum):
    ingreso = "ingreso"
    salida = "salida"


class NotaCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    tipo_movimiento: TipoMovimiento = Field(..., alias="tipoMovimiento")
    id_movimiento: int = Field(..., alias="idMovimiento")
    texto: str = Field(..., min_length=1, max_length=300)
    id_administrador: int = Field(..., alias="idAdministrador")  # hasta Fase 7


class NotaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id_nota: int = Field(serialization_alias="idNota")
    tipo_movimiento: TipoMovimiento = Field(serialization_alias="tipoMovimiento")
    id_movimiento: int = Field(serialization_alias="idMovimiento")
    texto: str
    id_administrador: int = Field(serialization_alias="idAdministrador")
    fecha: datetime
