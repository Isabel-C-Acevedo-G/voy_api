from fastapi import FastAPI

from app.models import rol_model, usuario_model  # noqa: F401  registra mappers
from app.routes import rol_routes, usuario_routes

app = FastAPI(
    title="VOY API",
    description="API REST para la gestión de parqueaderos de bicicletas (Medellín).",
    version="1.4.0",
)

app.include_router(rol_routes.router)
app.include_router(usuario_routes.router)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a VOY API"}
