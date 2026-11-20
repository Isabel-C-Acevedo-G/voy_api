# voy_api

API REST del sistema **VOY** — gestión de parqueaderos de bicicletas (Medellín).

## Requisitos

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)

## Instalación

```bash
uv sync
uv run alembic upgrade head
```

## Ejecución

```bash
uv run uvicorn app.main:app --reload
```

Documentación interactiva: http://127.0.0.1:8000/docs

## Reglas de negocio relevantes

### RN-009 — Historial permanente

Los **ingresos** y las **salidas** no se editan ni se eliminan. No existen `PUT`/`DELETE` sobre `/ingresos` ni `/salidas`. Las aclaraciones se harán con notas (fase posterior).

### Ingreso / salida

- `POST /ingresos` asigna automáticamente un espacio `libre` (RN-004) y lo marca `ocupado`.
- `POST /salidas` (o `PATCH /ingresos/{idIngreso}/salida`) exige las tres verificaciones en `true` (RN-007), cierra el ingreso y libera el espacio.
