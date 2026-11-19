"""Esquemas Pydantic para el recurso usuarios (Campos_Transacciones_voy)."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class TipoDocumento(str, Enum):
    CC = "CC"
    TI = "TI"
    CE = "CE"
    PA = "PA"


class EstadoUsuario(str, Enum):
    activo = "activo"
    inactivo = "inactivo"


class UsuarioCreate(BaseModel):
    """Alta de usuario (sin auth/JWT aún; claveHash llega en Fase 7)."""

    model_config = ConfigDict(populate_by_name=True)

    nombre: str = Field(..., min_length=1, max_length=100)
    tipo_documento: TipoDocumento = Field(..., alias="tipoDocumento")
    documento: str = Field(..., min_length=1, max_length=20)
    correo: EmailStr = Field(..., max_length=120)
    telefono: str | None = Field(default=None, max_length=20)
    id_rol: int = Field(..., alias="idRol")
    acepta_tratamiento_datos: bool = Field(..., alias="aceptaTratamientoDatos")
    estado: EstadoUsuario = EstadoUsuario.activo

    @field_validator("telefono")
    @classmethod
    def solo_digitos(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        if not value.isdigit():
            raise ValueError("telefono debe contener solo números")
        return value

    @field_validator("acepta_tratamiento_datos")
    @classmethod
    def debe_aceptar_tratamiento(cls, value: bool) -> bool:
        if value is not True:
            raise ValueError("aceptaTratamientoDatos debe ser true (Ley 1581)")
        return value


class UsuarioUpdate(BaseModel):
    """Actualización parcial (PATCH)."""

    model_config = ConfigDict(populate_by_name=True)

    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    telefono: str | None = Field(default=None, max_length=20)
    id_rol: int | None = Field(default=None, alias="idRol")
    estado: EstadoUsuario | None = None


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id_usuario: int = Field(serialization_alias="idUsuario")
    nombre: str
    tipo_documento: TipoDocumento = Field(serialization_alias="tipoDocumento")
    documento: str
    correo: EmailStr
    telefono: str | None = None
    id_rol: int = Field(serialization_alias="idRol")
    estado: EstadoUsuario
    acepta_tratamiento_datos: bool = Field(serialization_alias="aceptaTratamientoDatos")
    creado_en: datetime = Field(serialization_alias="creadoEn")
    actualizado_en: datetime | None = Field(default=None, serialization_alias="actualizadoEn")
    creado_por: int | None = Field(default=None, serialization_alias="creadoPor")
