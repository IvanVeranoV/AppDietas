import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, HTMLResponse

from src.database import engine, Base
from src.exceptions import ResourceNotFoundError, DatabaseError
import src.models  # Mantenemos esto para el mapeo de metadatos de SQLAlchemy
from .routers import categories, ingredients

from pathlib import Path

# Configuración básica del logger según tus directrices de AGENTS.md
logger = logging.getLogger("app.main")

app = FastAPI(
    title="AppDietas API",
    description="Backend para la gestión de dietas, ingredientes y menús",
    version="1.0.0"
)

# --- Manejadores Globales de Excepciones (Exception Handlers) ---

@app.exception_handler(ResourceNotFoundError)
async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError):
    """
    Captura automáticamente cualquier ResourceNotFoundError lanzado en el CRUD
    y lo transforma en una respuesta HTTP 404 limpia para el usuario.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    """
    Captura automáticamente cualquier DatabaseError y lo transforma en un 500.
    El error técnico ya se guardó en los logs dentro de la capa CRUD.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "A critical database error occurred. Please try again later."},
    )


# --- Registro de Rutas ---

app.include_router(ingredients.router, prefix="/ingredients")
app.include_router(categories.router, prefix="/categories")

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE_PATH = BASE_DIR / "welcome.html"

@app.get("/", response_class=HTMLResponse, tags=["Root"])
def read_root():
    """
    Renders the professional landing page by reading directly from a static HTML file.
    Follows AGENTS.md resource management guidelines using a context manager.
    """
    try:
        # Tu regla estricta: Uso obligatorio de context managers ('with') para recursos I/O
        with open(HTML_FILE_PATH, "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)
        
    except FileNotFoundError:
        logger.error(f"Welcome HTML file not found at path: {HTML_FILE_PATH}")
        # Fallback elegante en caso de que el archivo desaparezca por error
        return HTMLResponse(
            content="<h1>AppDietas API Operational</h1><p>Welcome file missing.</p>", 
            status_code=200
        )
    except Exception as e:
        logger.error("Unexpected error reading the welcome HTML file", exc_info=True)
        raise DatabaseError("Failed to load the API landing page.") from e