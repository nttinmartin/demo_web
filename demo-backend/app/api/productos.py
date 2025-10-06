
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.producto import Producto, ProductoCreate, ProductoUpdate
from app.db import crud
import aiosqlite

router = APIRouter()

@router.on_event("startup")
async def startup():
    await crud.init_db()

@router.get("/", response_model=List[Producto])
async def listar_productos():
    async with aiosqlite.connect(crud.DB_PATH) as db:
        cursor = await db.execute("SELECT id, nombre, sku, precio, stockActual, activo FROM productos")
        rows = await cursor.fetchall()
        return [Producto(id=row[0], nombre=row[1], sku=row[2], precio=row[3], stockActual=row[4], activo=bool(row[5])) for row in rows]

@router.post("/", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreate):
    async with aiosqlite.connect(crud.DB_PATH) as db:
        try:
            cursor = await db.execute(
                "INSERT INTO productos (nombre, sku, precio, stockActual, activo) VALUES (?, ?, ?, ?, ?)",
                (producto.nombre, producto.sku, producto.precio, producto.stockActual, producto.activo)
            )
            await db.commit()
            id = cursor.lastrowid
            return Producto(id=id, **producto.dict())
        except aiosqlite.IntegrityError:
            raise HTTPException(status_code=409, detail="SKU ya existe")

@router.patch("/{id}", response_model=Producto)
async def actualizar_producto(id: int, producto: ProductoUpdate):
    async with aiosqlite.connect(crud.DB_PATH) as db:
        await db.execute(
            "UPDATE productos SET nombre=?, sku=?, precio=?, stockActual=?, activo=? WHERE id=?",
            (producto.nombre, producto.sku, producto.precio, producto.stockActual, producto.activo, id)
        )
        await db.commit()
        return Producto(id=id, **producto.dict())

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(id: int):
    async with aiosqlite.connect(crud.DB_PATH) as db:
        await db.execute("DELETE FROM productos WHERE id=?", (id,))
        await db.commit()
    return None
