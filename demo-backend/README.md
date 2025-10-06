# Pedidos & Stock - Backend

Backend demo para la mini-app "Pedidos & Stock" usando Python, FastAPI y SQLite.

## Estructura
- FastAPI para API REST
- SQLite como base de datos embebida
- Modelos: Productos, Clientes, Pedidos, Líneas de Pedido
- Lógica de negocio y endpoints según especificación
- Pruebas unitarias y de API con pytest

## Instalación

1. Crear entorno virtual (opcional pero recomendado):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
2. Instalar dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
3. Configurar variables en `.env` si es necesario.

## Ejecución

```powershell
uvicorn app.main:app --reload
```

## Pruebas

```powershell
pytest
```

## Documentación interactiva

- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc
