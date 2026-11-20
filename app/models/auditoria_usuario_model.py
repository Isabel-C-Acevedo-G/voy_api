"""Auditoría de cambios de estado/rol de usuarios (RF-009)."""
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AuditoriaUsuario(Base):
    __tablename__ = "auditoria_usuarios"

    id_auditoria: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False, index=True)
    nuevo_estado: Mapped[str | None] = mapped_column(String(20), nullable=True)
    nuevo_rol: Mapped[int | None] = mapped_column(ForeignKey("roles.id_rol"), nullable=True)
    id_administrador: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False, index=True)
    fecha_cambio: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    motivo: Mapped[str] = mapped_column(String(200), nullable=False)

    usuario = relationship("Usuario", foreign_keys=[id_usuario])
    administrador = relationship("Usuario", foreign_keys=[id_administrador])
