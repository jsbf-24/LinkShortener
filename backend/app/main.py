from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import URLCreate, URLResponse
from app import database

app = FastAPI(title="AWS Link Shortener API")

# Configurar CORS para permitir peticiones desde el frontend (S3)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción puedes restringirlo al dominio de tu S3
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/shorten", response_model=URLResponse)
def shorten_url(payload: URLCreate, request: Request):
    item = database.create_url_record(payload.original_url)
    
    # Construir la URL corta utilizando la IP/dominio de la petición actual o EC2
    base_url = f"{request.url.scheme}://{request.client.host}:8000" # O usa tu IP pública de EC2 directamente
    # Una forma más robusta si estás detrás de un proxy es usar el header host:
    host = request.headers.get("host", "localhost:8000")
    short_url = f"{request.url.scheme}://{host}/{item['short_code']}"

    return {
        "short_code": item["short_code"],
        "original_url": item["original_url"],
        "short_url": short_url
    }

@app.get("/{short_code}")
def redirect_to_original(short_code: str):
    item = database.get_url_record(short_code)
    if not item:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Redirección HTTP 307 temporal
    return RedirectResponse(url=item["original_url"], status_code=307)

@app.get("/urls/{short_code}")
def get_url_info(short_code: str):
    item = database.get_url_record(short_code)
    if not item:
        raise HTTPException(status_code=404, detail="URL not found")
    return item