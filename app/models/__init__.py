"""Importa modelos para registrar mappers en Base.metadata."""
from app.models.rol_model import Rol
from app.models.usuario_model import Usuario

__all__ = ["Rol", "Usuario"]
