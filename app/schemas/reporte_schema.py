"""Esquemas de filtros/respuesta de reportes (RF-010)."""
from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class TipoReporte(str, Enum):
    ocupacion = "ocupacion"
    movimientos = "movimientos"
    usuarios_frecuentes = "usuarios_frecuentes"


class FormatoReporte(str, Enum):
    json = "json"
    csv = "csv"


class ReporteQuery(BaseModel):
    tipo: TipoReporte
    fecha_desde: date = Field(..., alias="fechaDesde")
    fecha_hasta: date = Field(..., alias="fechaHasta")
    formato: FormatoReporte = FormatoReporte.json

    model_config = {"populate_by_name": True}

    @model_validator(mode="after")
    def rango_fechas(self) -> "ReporteQuery":
        if self.fecha_desde > self.fecha_hasta:
            raise ValueError("fechaDesde no puede ser posterior a fechaHasta")
        return self
