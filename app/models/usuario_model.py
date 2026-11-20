"""Modelo ORM de usuarios (Campos_Transacciones_voy)."""
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_documento: Mapped[str] = mapped_column(String(2), nullable=False)
    documento: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    correo: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    clave_hash: Mapped[str] = mapped_column(String(255), nullable=False, default="", server_default="")
    id_rol: Mapped[int] = mapped_column(ForeignKey("roles.id_rol"), nullable=False, index=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="activo")
    acepta_tratamiento_datos: Mapped[bool] = mapped_column(Boolean, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    actualizado_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    creado_por: Mapped[int | None] = mapped_column(Integer, nullable=True)

    rol = relationship("Rol", back_populates="usuarios")

