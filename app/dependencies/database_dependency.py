"""Dependencia de base de datos: una sesión por petición HTTP."""
from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Crea una sesión, la entrega al endpoint y garantiza su cierre."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
