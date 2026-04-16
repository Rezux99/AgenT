# AgenT - FastAPI + Supabase

Proyecto base listo para Render. No necesitas programar.

## Qué hay aquí
- main.py: tu API con 2 rutas (/ y /health)
- requirements.txt: lo que Render instalará

## Pasos en Render
1. Sube esta carpeta a GitHub
2. En Render → New Web Service → conecta el repo
3. Build Command: pip install -r requirements.txt
4. Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
5. Variables de entorno:
   - SUPABASE_URL = (la de tu proyecto Supabase)
   - SUPABASE_KEY = (la service_role key)

Listo. Visita tu URL y verás {"mensaje":"funciona..."}
