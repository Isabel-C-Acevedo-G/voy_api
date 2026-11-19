from fastapi import FastAPI

from app.models import (  # noqa: F401
    bicicleta_model,
    espacio_model,
    ingreso_model,
    rol_model,
    usuario_model,
)
from app.routes import (
    bicicleta_routes,
    espacio_routes,
    ingreso_routes,
    rol_routes,
    usuario_routes,
)

app = FastAPI(
    title="VOY API",
    description="API REST para la gestión de parqueaderos de bicicletas (Medellín).",
    version="3.0.0",
)

app.include_router(rol_routes.router)
app.include_router(usuario_routes.router)
app.include_router(espacio_routes.router)
app.include_router(bicicleta_routes.router)
app.include_router(ingreso_routes.router)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a VOY API"}
