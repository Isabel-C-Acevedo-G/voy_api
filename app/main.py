from fastapi import FastAPI

from app.models import (  # noqa: F401
    auditoria_usuario_model,
    bicicleta_model,
    espacio_model,
    incidente_model,
    ingreso_model,
    nota_model,
    reserva_model,
    rol_model,
    salida_model,
    usuario_model,
)
from app.routes import (
    bicicleta_routes,
    espacio_routes,
    incidente_routes,
    ingreso_routes,
    nota_routes,
    reporte_routes,
    reserva_routes,
    rol_routes,
    salida_routes,
    usuario_routes,
)

app = FastAPI(
    title="VOY API",
    description="API REST para la gestión de parqueaderos de bicicletas (Medellín).",
    version="5.3.0",
)

app.include_router(rol_routes.router)
app.include_router(usuario_routes.router)
app.include_router(espacio_routes.router)
app.include_router(bicicleta_routes.router)
app.include_router(ingreso_routes.router)
app.include_router(salida_routes.router)
app.include_router(reserva_routes.router)
app.include_router(incidente_routes.router)
app.include_router(nota_routes.router)
app.include_router(reporte_routes.router)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a VOY API"}
