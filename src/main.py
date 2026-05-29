from .routers import categories, ingredients
from fastapi import FastAPI

from src.database import engine, Base
import src.models  # Recuerda dejar esto para que detecte las tablas


# Esta línea creará las tablas automáticamente si no existen en la base de datos
# Base.metadata.create_all(bind=engine)

# Esta es la instancia que Uvicorn busca
app = FastAPI()

app.include_router(ingredients.router, prefix="/ingredients")
app.include_router(categories.router, prefix="/categories")

@app.get("/")
def read_root():
    return {"message": "La API está funcionando correctamente jnad"}