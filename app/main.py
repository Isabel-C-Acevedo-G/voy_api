from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.auth import auth_routes
from app.middlewares.rate_limit import limiter
from app.middlewares.request_middleware import RequestMiddleware
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
    version="6.4.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(RequestMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
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
@limiter.limit("60/minute")
def read_root(request: Request):
    return {"message": "Bienvenido a VOY API"}
