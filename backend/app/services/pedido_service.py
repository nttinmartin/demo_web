from typing import List, Optional
from app.models.pedido import PedidoCreate, LineaPedido, Pedido
from app.models.producto import Producto
from app.models.cliente import Cliente
import os
import math

# Configuración desde entorno o valores por defecto
tasa_impuesto = float(os.getenv("TASA_IMPUESTO", 0.21))
tope_descuento = float(os.getenv("TOPE_DESCUENTO", 100.0))
cupon_summer10_activo = os.getenv("CUPON_SUMMER10_ACTIVO", "true").lower() == "true"

# Simulación de base de datos en memoria (reemplazar por persistencia real)
PRODUCTOS = {}
CLIENTES = {}
PEDIDOS = {}

# --- Lógica de negocio ---

def calcular_totales(lineas: List[LineaPedido], descuento: float = 0.0) -> dict:
    total_bruto = sum(l.cantidad * l.precioUnitario for l in lineas)
    impuestos = total_bruto * tasa_impuesto
    total_neto = total_bruto + impuestos - descuento
    return {
        "totalBruto": round(total_bruto, 2),
        "impuestos": round(impuestos, 2),
        "totalNeto": round(total_neto, 2)
    }

def aplicar_descuentos(lineas: List[LineaPedido], cupon: Optional[str], cliente: Optional[Cliente]) -> float:
    total_bruto = sum(l.cantidad * l.precioUnitario for l in lineas)
    descuento = 0.0
    tope = tope_descuento
    if cupon_summer10_activo and cupon == "SUMMER10":
        descuento += min(total_bruto * 0.10, tope)
    if cliente and cliente.segmento == "VIP":
        descuento += min(total_bruto * 0.05, tope)
    descuento = min(descuento, total_bruto * 0.20, tope)
    return round(descuento, 2)

def reservar_stock(lineas: List[LineaPedido]):
    for l in lineas:
        producto = PRODUCTOS.get(l.productoId)
        if not producto or producto.stockActual < l.cantidad:
            raise Exception(f"stock insuficiente para producto {l.productoId}")
        producto.stockActual -= l.cantidad

def reponer_stock(lineas: List[LineaPedido]):
    for l in lineas:
        producto = PRODUCTOS.get(l.productoId)
        if producto:
            producto.stockActual += l.cantidad

def confirmar_pedido(pedido_id: int):
    pedido = PEDIDOS.get(pedido_id)
    if not pedido:
        raise Exception("Pedido no encontrado")
    if pedido.estado != "BORRADOR":
        return pedido
    reservar_stock(pedido.lineas)
    pedido.estado = "CONFIRMADO"
    return pedido

def cancelar_pedido(pedido_id: int):
    pedido = PEDIDOS.get(pedido_id)
    if not pedido:
        raise Exception("Pedido no encontrado")
    if pedido.estado != "CONFIRMADO":
        return pedido
    reponer_stock(pedido.lineas)
    pedido.estado = "CANCELADO"
    return pedido

def puede_editar_lineas(pedido) -> bool:
    return pedido.estado not in ("ENVIADO",)
