"""Importa modelos para registrar mappers en Base.metadata."""
from app.models.espacio_model import Espacio
from app.models.rol_model import Rol
from app.models.usuario_model import Usuario

__all__ = ["Rol", "Usuario", "Espacio"]
