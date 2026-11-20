"""Modelo ORM de incidentes."""
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Incidente(Base):
    __tablename__ = "incidentes"

    id_incidente: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    id_bicicleta: Mapped[int | None] = mapped_column(
        ForeignKey("bicicletas.id_bicicleta"),
        nullable=True,
        index=True,
    )
    id_usuario_involucrado: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"),
        nullable=True,
        index=True,
    )
    foto: Mapped[str | None] = mapped_column(String(255), nullable=True)
    id_responsable: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False, index=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="abierto", index=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    bicicleta = relationship("Bicicleta", foreign_keys=[id_bicicleta])
    usuario_involucrado = relationship("Usuario", foreign_keys=[id_usuario_involucrado])
    responsable = relationship("Usuario", foreign_keys=[id_responsable])
