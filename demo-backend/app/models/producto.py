from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    sku: str
    precio: float
    stockActual: int
    activo: bool = True

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        orm_mode = True
