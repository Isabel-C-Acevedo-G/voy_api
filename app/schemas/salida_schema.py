"""Esquemas Pydantic para salidas (RF-005)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SalidaCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_ingreso: int = Field(..., alias="idIngreso")
    id_vigilante: int = Field(..., alias="idVigilante")  # hasta Fase 7 (JWT)
    verificacion_marca: bool = Field(..., alias="verificacionMarca")
    verificacion_color: bool = Field(..., alias="verificacionColor")
    verificacion_serie: bool = Field(..., alias="verificacionSerie")
    nota: str | None = Field(default=None, max_length=300)

    @model_validator(mode="after")
    def tres_verificaciones(self) -> "SalidaCreate":
        if not (self.verificacion_marca and self.verificacion_color and self.verificacion_serie):
            raise ValueError(
                "verificacionMarca, verificacionColor y verificacionSerie deben ser true (RN-007)"
            )
        return self


class SalidaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id_salida: int = Field(serialization_alias="idSalida")
    id_ingreso: int = Field(serialization_alias="idIngreso")
    fecha_salida: datetime = Field(serialization_alias="fechaSalida")
    id_vigilante: int = Field(serialization_alias="idVigilante")
    verificacion_marca: bool = Field(serialization_alias="verificacionMarca")
    verificacion_color: bool = Field(serialization_alias="verificacionColor")
    verificacion_serie: bool = Field(serialization_alias="verificacionSerie")
    duracion_minutos: int | None = Field(default=None, serialization_alias="duracionMinutos")
    nota: str | None = None
    creado_en: datetime = Field(serialization_alias="creadoEn")
