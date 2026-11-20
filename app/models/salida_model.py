"""Modelo ORM de salidas del parqueadero."""
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Salida(Base):
    __tablename__ = "salidas"

    id_salida: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_ingreso: Mapped[int] = mapped_column(
        ForeignKey("ingresos.id_ingreso"),
        unique=True,
        nullable=False,
        index=True,
    )
    fecha_salida: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    id_vigilante: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False, index=True)
    verificacion_marca: Mapped[bool] = mapped_column(Boolean, nullable=False)
    verificacion_color: Mapped[bool] = mapped_column(Boolean, nullable=False)
    verificacion_serie: Mapped[bool] = mapped_column(Boolean, nullable=False)
    duracion_minutos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    nota: Mapped[str | None] = mapped_column(String(300), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    ingreso = relationship("Ingreso")
    vigilante = relationship("Usuario")
