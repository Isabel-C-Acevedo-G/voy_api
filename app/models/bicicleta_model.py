"""Modelo ORM de bicicletas."""
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Bicicleta(Base):
    __tablename__ = "bicicletas"

    id_bicicleta: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_propietario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"),
        nullable=False,
        index=True,
    )
    marca: Mapped[str] = mapped_column(String(50), nullable=False)
    modelo: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=False)
    tipo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    numero_serie: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    foto: Mapped[str | None] = mapped_column(String(255), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="activa")
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    actualizado_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    propietario = relationship("Usuario")
