"""Modelo ORM de ingresos al parqueadero."""
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Ingreso(Base):
    __tablename__ = "ingresos"

    id_ingreso: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_bicicleta: Mapped[int] = mapped_column(ForeignKey("bicicletas.id_bicicleta"), nullable=False, index=True)
    id_espacio: Mapped[int] = mapped_column(ForeignKey("espacios.id_espacio"), nullable=False, index=True)
    # FK a reservas se añade en Fase 5; por ahora solo entero nullable
    id_reserva: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fecha_ingreso: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    id_vigilante: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False, index=True)
    observaciones: Mapped[str | None] = mapped_column(String(200), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="activo", index=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    bicicleta = relationship("Bicicleta")
    espacio = relationship("Espacio")
    vigilante = relationship("Usuario")
