from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import create_db_and_tables
from backend.routers import categorias, ingredientes, productos, usuarios, pedidos, direcciones, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Parcial UTN — Sistema de Productos", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categorias.router)
app.include_router(ingredientes.router)
app.include_router(productos.router)
app.include_router(usuarios.router)
app.include_router(pedidos.router)
app.include_router(direcciones.router)
app.include_router(admin.router)
