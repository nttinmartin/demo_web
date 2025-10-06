from app.models.cliente import Cliente, ClienteCreate, ClienteUpdate
from typing import Dict

CLIENTES: Dict[int, Cliente] = {}
EMAIL_SET = set()

def crear_cliente(data: ClienteCreate) -> Cliente:
    if data.email in EMAIL_SET:
        raise Exception("Email ya registrado")
    new_id = max(CLIENTES.keys(), default=0) + 1
    cliente = Cliente(id=new_id, **data.dict())
    CLIENTES[new_id] = cliente
    EMAIL_SET.add(data.email)
    return cliente

def actualizar_cliente(id: int, data: ClienteUpdate) -> Cliente:
    if id not in CLIENTES:
        raise Exception("Cliente no encontrado")
    if data.email != CLIENTES[id].email and data.email in EMAIL_SET:
        raise Exception("Email ya registrado")
    EMAIL_SET.discard(CLIENTES[id].email)
    EMAIL_SET.add(data.email)
    cliente = Cliente(id=id, **data.dict())
    CLIENTES[id] = cliente
    return cliente

def eliminar_cliente(id: int):
    if id in CLIENTES:
        EMAIL_SET.discard(CLIENTES[id].email)
        del CLIENTES[id]

def listar_clientes():
    return list(CLIENTES.values())
