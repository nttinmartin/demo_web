
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.pedido import Pedido, PedidoCreate, LineaPedido
from app.db import crud
import aiosqlite
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[Pedido])
async def listar_pedidos():
    async with aiosqlite.connect(crud.DB_PATH) as db:
        cursor = await db.execute("SELECT id, clienteId, estado, totalBruto, impuestos, descuento, totalNeto, creadoEn FROM pedidos")
        rows = await cursor.fetchall()
        pedidos = []
        for row in rows:
            pedidos.append(Pedido(
                id=row[0], clienteId=row[1], estado=row[2], totalBruto=row[3], impuestos=row[4], descuento=row[5], totalNeto=row[6], creadoEn=row[7], lineas=[]
            ))
        return pedidos

@router.post("/", response_model=Pedido, status_code=status.HTTP_201_CREATED)
async def crear_pedido(pedido: PedidoCreate):
    async with aiosqlite.connect(crud.DB_PATH) as db:
        now = datetime.now().isoformat()
        cursor = await db.execute(
            "INSERT INTO pedidos (clienteId, estado, totalBruto, impuestos, descuento, totalNeto, creadoEn) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pedido.clienteId, pedido.estado, 0, 0, pedido.descuento, 0, now)
        )
        await db.commit()
        id = cursor.lastrowid
        return Pedido(id=id, clienteId=pedido.clienteId, estado=pedido.estado, totalBruto=0, impuestos=0, descuento=pedido.descuento, totalNeto=0, creadoEn=now, lineas=[])

@router.post("/{id}/lineas", response_model=Pedido)
async def agregar_linea_pedido(id: int, linea: LineaPedido):
    async with aiosqlite.connect(crud.DB_PATH) as db:
        await db.execute(
            "INSERT INTO lineas_pedido (pedidoId, productoId, cantidad, precioUnitario) VALUES (?, ?, ?, ?)",
            (id, linea.productoId, linea.cantidad, linea.precioUnitario)
        )
        await db.commit()
        # Retornar pedido actualizado (simplificado)
        return await obtener_pedido(id)

async def obtener_pedido(id: int) -> Pedido:
    async with aiosqlite.connect(crud.DB_PATH) as db:
        cursor = await db.execute("SELECT id, clienteId, estado, totalBruto, impuestos, descuento, totalNeto, creadoEn FROM pedidos WHERE id=?", (id,))
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        cursor = await db.execute("SELECT productoId, cantidad, precioUnitario FROM lineas_pedido WHERE pedidoId=?", (id,))
        lineas = [LineaPedido(productoId=l[0], cantidad=l[1], precioUnitario=l[2]) for l in await cursor.fetchall()]
        return Pedido(id=row[0], clienteId=row[1], estado=row[2], totalBruto=row[3], impuestos=row[4], descuento=row[5], totalNeto=row[6], creadoEn=row[7], lineas=lineas)

@router.post("/{id}/confirmar", response_model=Pedido)
async def confirmar_pedido(id: int):
    # Aquí se debe implementar la lógica de reserva de stock y actualización de totales
    # Por simplicidad, solo cambia el estado
    async with aiosqlite.connect(crud.DB_PATH) as db:
        await db.execute("UPDATE pedidos SET estado=? WHERE id=?", ("CONFIRMADO", id))
        await db.commit()
        return await obtener_pedido(id)

@router.post("/{id}/enviar", response_model=Pedido)
async def enviar_pedido(id: int):
    async with aiosqlite.connect(crud.DB_PATH) as db:
        await db.execute("UPDATE pedidos SET estado=? WHERE id=?", ("ENVIADO", id))
        await db.commit()
        return await obtener_pedido(id)

@router.post("/{id}/cancelar", response_model=Pedido)
async def cancelar_pedido(id: int):
    async with aiosqlite.connect(crud.DB_PATH) as db:
        await db.execute("UPDATE pedidos SET estado=? WHERE id=?", ("CANCELADO", id))
        await db.commit()
        return await obtener_pedido(id)
