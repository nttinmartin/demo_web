from app.models.producto import Producto, ProductoCreate, ProductoUpdate
from typing import Dict

PRODUCTOS: Dict[int, Producto] = {}

# SKU único
SKU_SET = set()


def crear_producto(data: ProductoCreate) -> Producto:
    if data.sku in SKU_SET:
        raise Exception("SKU ya existe")
    new_id = max(PRODUCTOS.keys(), default=0) + 1
    producto = Producto(id=new_id, **data.dict())
    PRODUCTOS[new_id] = producto
    SKU_SET.add(data.sku)
    return producto

def actualizar_producto(id: int, data: ProductoUpdate) -> Producto:
    if id not in PRODUCTOS:
        raise Exception("Producto no encontrado")
    if data.sku != PRODUCTOS[id].sku and data.sku in SKU_SET:
        raise Exception("SKU ya existe")
    SKU_SET.discard(PRODUCTOS[id].sku)
    SKU_SET.add(data.sku)
    producto = Producto(id=id, **data.dict())
    PRODUCTOS[id] = producto
    return producto

def eliminar_producto(id: int):
    if id in PRODUCTOS:
        SKU_SET.discard(PRODUCTOS[id].sku)
        del PRODUCTOS[id]

def listar_productos():
    return list(PRODUCTOS.values())
