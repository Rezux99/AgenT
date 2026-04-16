from fastapi import FastAPI
from supabase import create_client
import os

app = FastAPI(title="AgenT")

# Render te dará estas dos variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def hola():
    return {"mensaje": "funciona - FastAPI + Supabase listo"}

@app.get("/health")
def health():
    return {"ok": True, "supabase_conectado": bool(supabase)}
