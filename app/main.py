from fastapi import FastAPI

from app.models import espacio_model, rol_model, usuario_model  # noqa: F401
from app.routes import espacio_routes, rol_routes, usuario_routes

app = FastAPI(
    title="VOY API",
    description="API REST para la gestión de parqueaderos de bicicletas (Medellín).",
    version="2.0.0",
)

app.include_router(rol_routes.router)
app.include_router(usuario_routes.router)
app.include_router(espacio_routes.router)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a VOY API"}
