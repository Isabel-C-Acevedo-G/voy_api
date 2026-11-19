from fastapi import FastAPI

# Instancia principal de la aplicación
app = FastAPI(
    title="VOY API",
    description="API REST para la gestión de parqueaderos de bicicletas (Medellín).",
    version="0.2.0",
)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a VOY API"}
