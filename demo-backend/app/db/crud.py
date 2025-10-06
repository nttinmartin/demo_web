import aiosqlite
from typing import Any, List, Dict
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db.sqlite3"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            sku TEXT UNIQUE NOT NULL,
            precio REAL NOT NULL,
            stockActual INTEGER NOT NULL,
            activo BOOLEAN NOT NULL
        );
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            segmento TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clienteId INTEGER NOT NULL,
            estado TEXT NOT NULL,
            totalBruto REAL NOT NULL,
            impuestos REAL NOT NULL,
            descuento REAL NOT NULL,
            totalNeto REAL NOT NULL,
            creadoEn TEXT NOT NULL,
            FOREIGN KEY(clienteId) REFERENCES clientes(id)
        );
        CREATE TABLE IF NOT EXISTS lineas_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedidoId INTEGER NOT NULL,
            productoId INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precioUnitario REAL NOT NULL,
            FOREIGN KEY(pedidoId) REFERENCES pedidos(id),
            FOREIGN KEY(productoId) REFERENCES productos(id)
        );
        ''')
        await db.commit()
