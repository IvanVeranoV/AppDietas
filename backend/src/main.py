import logging
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse

from src.exceptions import DatabaseError, ResourceNotFoundError

from .routers import categories, ingredients, menus, recipe_ingredients, recipes, users

# Configuración básica del logger según tus directrices de AGENTS.md
logger = logging.getLogger("app.main")

app = FastAPI(docs_url=None)  # Desactivamos el por defecto para que no choque


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{app.title} - Swagger UI (Dark Fixed)</title>
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-themes@3.0.1/themes/3.x/theme-monokai.css">
    
    <style>
        body {{
            background-color: #272822 !important;
        }}
        
        .swagger-ui .info .title, 
        .swagger-ui .opblock-tag, 
        .swagger-ui .opblock .opblock-summary-description,
        .swagger-ui .tabli,
        .swagger-ui .response-col_status,
        .swagger-ui table thead tr th,
        .swagger-ui .response-col_links {{
            color: #f8f8f2 !important;
        }}
        
        .swagger-ui .opblock-description-wrapper p, 
        .swagger-ui .opblock-external-docs-wrapper p, 
        .swagger-ui .opblock-title_normal p,
        .swagger-ui .response-col_description__inner,
        .swagger-ui .response-col_description {{
            color: #e6db74 !important; /* Un tono amarillo/crema muy legible en Monokai */
        }}

        .swagger-ui .arrow {{
            fill: #f8f8f2 !important;
        }}
        
        .swagger-ui .responses-table_clean h4, 
        .swagger-ui .responses-table_clean h5 {{
            color: #ae81ff !important;
        }}
    </style>
    </head>
    <body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        const ui = SwaggerUIBundle({{
            url: '{app.openapi_url}',
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
            ],
            layout: "BaseLayout",
            deepLinking: true,
            syntaxHighlight: {{ theme: "monokai" }}
        }});
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


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
        content={
            "detail": "A critical database error occurred. Please try again later."
        },
    )


# --- Registro de Rutas ---

app.include_router(ingredients.router, prefix="/ingredients")
app.include_router(categories.router, prefix="/categories")
app.include_router(recipes.router, prefix="/recipes")
app.include_router(recipe_ingredients.router, prefix="/recipe-ingredients")
app.include_router(users.router, prefix="/users")
app.include_router(menus.router, prefix="/menus")

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
            status_code=200,
        )
    except Exception as e:
        logger.error("Unexpected error reading the welcome HTML file", exc_info=True)
        raise DatabaseError("Failed to load the API landing page.") from e
