"""Modelo ORM de notas sobre ingresos/salidas."""
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Nota(Base):
    __tablename__ = "notas"

    id_nota: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tipo_movimiento: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    id_movimiento: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    texto: Mapped[str] = mapped_column(String(300), nullable=False)
    id_administrador: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False, index=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    administrador = relationship("Usuario")
