import os
from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from supabase import create_client, Client

app = FastAPI()


# ----- Modelos -----
class Mensaje(BaseModel):
    id: int
    created_at: str
    rol: str
    contenido: str


# ----- Supabase lazy client -----
_supabase_client: Client | None = None


def get_supabase() -> Client:
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        # Esto evita que el import falle si las env vars no están en build;
        # solo falla si realmente llamas a una ruta que usa Supabase.
        raise HTTPException(
            status_code=500,
            detail="Config de Supabase incompleta (SUPABASE_URL o SUPABASE_KEY).",
        )

    _supabase_client = create_client(url, key)
    return _supabase_client


# ----- Rutas -----
@app.get("/")
def root():
    return {"mensaje": "funciona"}


@app.post("/mensaje")
def crear_mensaje(
    rol: str = Query(..., description="Rol del emisor, p.ej. 'yo'"),
    contenido: str = Query(..., description="Contenido del mensaje"),
    supabase: Client = Depends(get_supabase),
):
    data = {"rol": rol, "contenido": contenido}
    try:
        resp = supabase.table("mensajes").insert(data).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar mensaje: {e}")

    # supabase-py devuelve .data como lista de filas insertadas
    if not getattr(resp, "data", None):
        raise HTTPException(status_code=500, detail="Insert no devolvió datos.")

    return {"ok": True, "mensaje": resp.data[0]}


@app.get("/mensajes", response_model=List[Mensaje])
def listar_mensajes(supabase: Client = Depends(get_supabase)):
    try:
        resp = supabase.table("mensajes").select("*").order("created_at").execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer mensajes: {e}")

    return resp.data