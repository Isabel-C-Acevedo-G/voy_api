# voy_api

API REST del sistema **VOY** — gestión de parqueaderos de bicicletas (Medellín).

Stack: **FastAPI** · **Pydantic v2** · **SQLAlchemy** · **Alembic** · **JWT (OAuth2)** · **bcrypt**.

## Requisitos

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)

## Instalación

```bash
uv sync
copy .env.example .env   # Windows; ajusta SECRET_KEY
uv run alembic upgrade head
```

## Ejecución

```bash
uv run uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000  
- Swagger: http://127.0.0.1:8000/docs  

Al arrancar se crean (si no existen) los roles: `ciclista`, `vigilante`, `administrador`.

## Autenticación

| Método | Path | Notas |
|--------|------|--------|
| `POST` | `/auth/register` | Alta con `clave` (se guarda solo el hash). Rol por defecto: `ciclista`. |
| `POST` | `/auth/login` | Form OAuth2: `username` = correo o documento, `password` = clave. JWT **30 min**. |
| `GET` | `/auth/me` | Usuario del token (`Authorization: Bearer …`). |

**No existe** `POST /usuarios` para alta: usar siempre `/auth/register`.

### Roles

| Rol | Uso típico |
|-----|------------|
| `ciclista` | Registro, bicicletas propias, reservas |
| `vigilante` | Ingresos, salidas, incidentes |
| `administrador` | Usuarios, espacios, notas, reportes, desactivar bicicletas |

## Endpoints principales

| Recurso | Paths |
|---------|--------|
| Roles | `GET/POST /roles` |
| Usuarios | `GET/PATCH /usuarios`, `PATCH /usuarios/{id}/gestion` |
| Espacios | `GET/POST/PATCH /espacios` |
| Bicicletas | `GET/POST/PATCH /bicicletas`, `PATCH …/estado` |
| Ingresos | `GET/POST /ingresos`, `PATCH /ingresos/{id}/salida` |
| Salidas | `GET/POST /salidas` |
| Reservas | `GET/POST /reservas`, `PATCH …/cancelar` |
| Incidentes | `GET/POST/PATCH /incidentes` |
| Notas | `GET/POST /notas` |
| Reportes | `GET /reportes?tipo=&fechaDesde=&fechaHasta=&formato=` |

JSON en **camelCase** (`idUsuario`, `numeroSerie`, …).

## Variables de entorno (`.env`)

```env
DATABASE_URL=sqlite:///./voy.db
SECRET_KEY=cambia-esta-clave-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Git / versiones

Trabajo en `develop`; entrega en `main` con tag **`v1.0.0`**. Tags intermedios `v0.1` … `v6.4` siguen el plan de implementación por fases.
