from fastapi import FastAPI
from supabase import create_client
import os

app = FastAPI(title="AgenT")

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@app.get("/")
def hola():
    return {"mensaje": "funciona"}

@app.post("/mensaje")
def guardar(rol: str, contenido: str):
    supabase.table("mensajes").insert({"rol": rol, "contenido": contenido}).execute()
    return {"ok": True}

@app.get("/mensajes")
def listar():
    data = supabase.table("mensajes").select("*").order("id", desc=True).limit(20).execute()
    return data.data
