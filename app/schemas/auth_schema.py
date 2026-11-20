"""Schemas de autenticación."""
import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.usuario_schema import TipoDocumento


class UsuarioRegister(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nombre: str = Field(..., min_length=1, max_length=100)
    tipo_documento: TipoDocumento = Field(..., alias="tipoDocumento")
    documento: str = Field(..., min_length=1, max_length=20)
    correo: EmailStr = Field(..., max_length=120)
    telefono: str | None = Field(default=None, max_length=20)
    clave: str = Field(..., min_length=8, max_length=72, alias="clave")
    id_rol: int | None = Field(default=None, alias="idRol")
    acepta_tratamiento_datos: bool = Field(..., alias="aceptaTratamientoDatos")

    @field_validator("clave")
    @classmethod
    def password_segura(cls, value: str) -> str:
        if " " in value:
            raise ValueError("La contraseña no puede contener espacios")
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe incluir una mayúscula")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe incluir una minúscula")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe incluir un número")
        return value

    @field_validator("acepta_tratamiento_datos")
    @classmethod
    def debe_aceptar(cls, value: bool) -> bool:
        if value is not True:
            raise ValueError("aceptaTratamientoDatos debe ser true")
        return value


class TokenResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    access_token: str
    token_type: str = "bearer"
    rol: str
    expira_en: datetime = Field(serialization_alias="expiraEn")


class TokenData(BaseModel):
    sub: str | None = None
    rol: str | None = None
