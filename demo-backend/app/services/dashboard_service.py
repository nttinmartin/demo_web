from typing import Dict, List
from app.models.pedido import Pedido
from app.models.producto import Producto
from datetime import datetime, timedelta

# Simulación de datos en memoria
PEDIDOS: Dict[int, Pedido] = {}
PRODUCTOS: Dict[int, Producto] = {}


def metricas_dashboard() -> dict:
    pedidos_por_estado = {}
    for p in PEDIDOS.values():
        pedidos_por_estado[p.estado] = pedidos_por_estado.get(p.estado, 0) + 1
    # Top productos últimos 7 días
    hace_7d = datetime.now() - timedelta(days=7)
    ventas = {}
    for p in PEDIDOS.values():
        if p.creadoEn and p.creadoEn >= hace_7d:
            for l in p.lineas:
                ventas[l.productoId] = ventas.get(l.productoId, 0) + l.cantidad
    top_productos = sorted(ventas.items(), key=lambda x: x[1], reverse=True)[:5]
    return {
        "pedidosPorEstado": pedidos_por_estado,
        "topProductos": top_productos
    }
