
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.cliente import Cliente, ClienteCreate, ClienteUpdate
from app.db import crud
import aiosqlite

router = APIRouter()

@router.get("/", response_model=List[Cliente])
async def listar_clientes():
    async with aiosqlite.connect(crud.DB_PATH) as db:
        cursor = await db.execute("SELECT id, nombre, email, segmento FROM clientes")
        rows = await cursor.fetchall()
        return [Cliente(id=row[0], nombre=row[1], email=row[2], segmento=row[3]) for row in rows]

@router.post("/", response_model=Cliente, status_code=status.HTTP_201_CREATED)
async def crear_cliente(cliente: ClienteCreate):
    async with aiosqlite.connect(crud.DB_PATH) as db:
        try:
            cursor = await db.execute(
                "INSERT INTO clientes (nombre, email, segmento) VALUES (?, ?, ?)",
                (cliente.nombre, cliente.email, cliente.segmento)
            )
            await db.commit()
            id = cursor.lastrowid
            return Cliente(id=id, **cliente.dict())
        except aiosqlite.IntegrityError:
            raise HTTPException(status_code=409, detail="Email ya registrado")

@router.patch("/{id}", response_model=Cliente)
async def actualizar_cliente(id: int, cliente: ClienteUpdate):
    async with aiosqlite.connect(crud.DB_PATH) as db:
        await db.execute(
            "UPDATE clientes SET nombre=?, email=?, segmento=? WHERE id=?",
            (cliente.nombre, cliente.email, cliente.segmento, id)
        )
        await db.commit()
        return Cliente(id=id, **cliente.dict())

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_cliente(id: int):
    async with aiosqlite.connect(crud.DB_PATH) as db:
        await db.execute("DELETE FROM clientes WHERE id=?", (id,))
        await db.commit()
    return None
