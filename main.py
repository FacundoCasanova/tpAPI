from fastapi import FastAPI
from database import init_db
import autos
import ventas

app = FastAPI(
    title="API de Ventas de Autos",
    description="Trabajo Práctico Programación IV - Gestión de Autos y Ventas",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(autos.router)
app.include_router(ventas.router)


@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Ventas de Autos. Visita /docs para la documentación."}