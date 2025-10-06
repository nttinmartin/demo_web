from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import productos, clientes, pedidos, ajustes

app = FastAPI(title="Pedidos & Stock API", version="1.0.0")

# Middleware CORS para desarrollo
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(productos.router, prefix="/productos", tags=["Productos"])
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(ajustes.router, prefix="/ajustes", tags=["Ajustes"])
