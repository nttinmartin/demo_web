from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LineaPedido(BaseModel):
    productoId: int
    cantidad: int
    precioUnitario: float

class PedidoBase(BaseModel):
    clienteId: int
    estado: str
    descuento: float = 0.0
    creadoEn: Optional[datetime] = None
    lineas: List[LineaPedido] = []

class PedidoCreate(PedidoBase):
    pass

class Pedido(PedidoBase):
    id: int
    totalBruto: float
    impuestos: float
    totalNeto: float

    class Config:
        orm_mode = True
