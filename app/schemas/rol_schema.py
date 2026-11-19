"""Esquemas Pydantic para el recurso roles."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RolCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50, examples=["ciclista"])


class RolResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id_rol: int = Field(serialization_alias="idRol")
    nombre: str
    creado_en: datetime = Field(serialization_alias="creadoEn")
