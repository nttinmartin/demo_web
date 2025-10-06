from pydantic import BaseModel, EmailStr

class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    segmento: str

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int

    class Config:
        orm_mode = True
