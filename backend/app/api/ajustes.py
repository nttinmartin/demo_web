from fastapi import APIRouter
from app.db import crud
import os

router = APIRouter()

@router.get("/")
async def obtener_ajustes():
    return {
        "tasaImpuesto": float(os.getenv("TASA_IMPUESTO", 0.21)),
        "topeDescuento": float(os.getenv("TOPE_DESCUENTO", 100.0)),
        "cuponSummer10Activo": os.getenv("CUPON_SUMMER10_ACTIVO", "true").lower() == "true"
    }

@router.post("/initdb")
async def init_db():
    await crud.init_db()
    return {"ok": True}
