"""Endpoints de reportes (RF-010)."""
from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.reporte_schema import FormatoReporte, TipoReporte
from app.services import reporte_service

router = APIRouter(prefix="/reportes", tags=["reportes"])


@router.get("")
def generar_reporte(
    tipo: TipoReporte = Query(...),
    fechaDesde: date = Query(...),
    fechaHasta: date = Query(...),
    formato: FormatoReporte = Query(FormatoReporte.json),
    db: Session = Depends(get_db),
):
    if fechaDesde > fechaHasta:
        return JSONResponse(
            status_code=422,
            content={"detail": "fechaDesde no puede ser posterior a fechaHasta"},
        )

    data = reporte_service.generar_reporte(db, tipo, fechaDesde, fechaHasta)
    if formato == FormatoReporte.csv:
        csv_text = reporte_service.reporte_a_csv(data)
        return PlainTextResponse(content=csv_text, media_type="text/csv")
    return data
