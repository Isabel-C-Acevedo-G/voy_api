"""Reportes calculados al vuelo (RF-010)."""
from datetime import date, datetime, time, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.bicicleta_model import Bicicleta
from app.models.espacio_model import Espacio
from app.models.ingreso_model import Ingreso
from app.models.salida_model import Salida
from app.models.usuario_model import Usuario
from app.schemas.reporte_schema import TipoReporte


def _rango(fecha_desde: date, fecha_hasta: date) -> tuple[datetime, datetime]:
    inicio = datetime.combine(fecha_desde, time.min, tzinfo=timezone.utc)
    fin = datetime.combine(fecha_hasta, time.max, tzinfo=timezone.utc)
    return inicio, fin


def generar_reporte(
    db: Session,
    tipo: TipoReporte,
    fecha_desde: date,
    fecha_hasta: date,
) -> dict:
    inicio, fin = _rango(fecha_desde, fecha_hasta)

    if tipo == TipoReporte.ocupacion:
        total = db.query(Espacio).filter(Espacio.activo.is_(True)).count()
        por_estado = (
            db.query(Espacio.estado, func.count(Espacio.id_espacio))
            .filter(Espacio.activo.is_(True))
            .group_by(Espacio.estado)
            .all()
        )
        return {
            "tipo": tipo.value,
            "fechaDesde": str(fecha_desde),
            "fechaHasta": str(fecha_hasta),
            "totalEspaciosActivos": total,
            "porEstado": {estado: count for estado, count in por_estado},
        }

    if tipo == TipoReporte.movimientos:
        ingresos = (
            db.query(Ingreso)
            .filter(Ingreso.fecha_ingreso >= inicio, Ingreso.fecha_ingreso <= fin)
            .count()
        )
        salidas = (
            db.query(Salida)
            .filter(Salida.fecha_salida >= inicio, Salida.fecha_salida <= fin)
            .count()
        )
        return {
            "tipo": tipo.value,
            "fechaDesde": str(fecha_desde),
            "fechaHasta": str(fecha_hasta),
            "totalIngresos": ingresos,
            "totalSalidas": salidas,
        }

    filas = (
        db.query(
            Usuario.id_usuario,
            Usuario.nombre,
            Usuario.correo,
            func.count(Ingreso.id_ingreso).label("ingresos"),
        )
        .join(Bicicleta, Bicicleta.id_propietario == Usuario.id_usuario)
        .join(Ingreso, Ingreso.id_bicicleta == Bicicleta.id_bicicleta)
        .filter(Ingreso.fecha_ingreso >= inicio, Ingreso.fecha_ingreso <= fin)
        .group_by(Usuario.id_usuario, Usuario.nombre, Usuario.correo)
        .order_by(func.count(Ingreso.id_ingreso).desc())
        .limit(20)
        .all()
    )
    return {
        "tipo": tipo.value,
        "fechaDesde": str(fecha_desde),
        "fechaHasta": str(fecha_hasta),
        "usuarios": [
            {
                "idUsuario": row.id_usuario,
                "nombre": row.nombre,
                "correo": row.correo,
                "ingresos": row.ingresos,
            }
            for row in filas
        ],
    }


def reporte_a_csv(data: dict) -> str:
    tipo = data.get("tipo")
    lines = [
        f"tipo,{tipo}",
        f"fechaDesde,{data.get('fechaDesde')}",
        f"fechaHasta,{data.get('fechaHasta')}",
    ]
    if tipo == "ocupacion":
        lines.append("totalEspaciosActivos," + str(data.get("totalEspaciosActivos", 0)))
        lines.append("estado,cantidad")
        for estado, cantidad in (data.get("porEstado") or {}).items():
            lines.append(f"{estado},{cantidad}")
    elif tipo == "movimientos":
        lines.append(f"totalIngresos,{data.get('totalIngresos', 0)}")
        lines.append(f"totalSalidas,{data.get('totalSalidas', 0)}")
    else:
        lines.append("idUsuario,nombre,correo,ingresos")
        for u in data.get("usuarios") or []:
            lines.append(f"{u['idUsuario']},{u['nombre']},{u['correo']},{u['ingresos']}")
    return "\n".join(lines) + "\n"
