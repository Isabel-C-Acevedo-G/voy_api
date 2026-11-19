"""Esquemas Pydantic para bicicletas (RF-003)."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TipoBicicleta(str, Enum):
    urbana = "urbana"
    montana = "montaña"
    ruta = "ruta"
    electrica = "eléctrica"
    otra = "otra"


class EstadoBicicleta(str, Enum):
    activa = "activa"
    inactiva = "inactiva"


class BicicletaCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_propietario: int = Field(..., alias="idPropietario")
    marca: str = Field(..., min_length=1, max_length=50)
    modelo: str = Field(..., min_length=1, max_length=50)
    color: str = Field(..., min_length=1, max_length=50)
    tipo: TipoBicicleta | None = None
    numero_serie: str = Field(..., min_length=1, max_length=40, alias="numeroSerie")
    foto: str | None = Field(default=None, max_length=255)

    @field_validator("foto")
    @classmethod
    def foto_jpg_png(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        lower = value.lower()
        if not (lower.endswith(".jpg") or lower.endswith(".jpeg") or lower.endswith(".png")):
            raise ValueError("foto debe ser ruta .jpg o .png")
        return value


class BicicletaUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    marca: str | None = Field(default=None, min_length=1, max_length=50)
    modelo: str | None = Field(default=None, min_length=1, max_length=50)
    color: str | None = Field(default=None, min_length=1, max_length=50)
    tipo: TipoBicicleta | None = None
    foto: str | None = Field(default=None, max_length=255)

    @field_validator("foto")
    @classmethod
    def foto_jpg_png(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        lower = value.lower()
        if not (lower.endswith(".jpg") or lower.endswith(".jpeg") or lower.endswith(".png")):
            raise ValueError("foto debe ser ruta .jpg o .png")
        return value


class BicicletaEstadoUpdate(BaseModel):
    estado: EstadoBicicleta


class BicicletaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id_bicicleta: int = Field(serialization_alias="idBicicleta")
    id_propietario: int = Field(serialization_alias="idPropietario")
    marca: str
    modelo: str
    color: str
    tipo: TipoBicicleta | None = None
    numero_serie: str = Field(serialization_alias="numeroSerie")
    foto: str | None = None
    estado: EstadoBicicleta
    creado_en: datetime = Field(serialization_alias="creadoEn")
    actualizado_en: datetime | None = Field(default=None, serialization_alias="actualizadoEn")
