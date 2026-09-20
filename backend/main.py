import sys
from pathlib import Path
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import CORS_ORIGINS

from extractor import extract_text_from_pdf
from storage import get_file_path

from routes import export, extract, upload, validate


router = APIRouter()

app = FastAPI(title="Copiloto Documentos")

app.include_router(upload.router, prefix="/api")
app.include_router(extract.router, prefix="/api")
app.include_router(validate.router, prefix="/api")
app.include_router(export.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.get("/extract-text/{file_id}")
def extract_text(file_id: str):
    file_path = get_file_path(file_id)

    if file_path.suffix.lower() != ".pdf":
        return {
            "detail": "La extracción de imágenes todavía no está implementada."
        }

    text = extract_text_from_pdf(file_path)

    return {
        "file_id": file_id,
        "text": text,
    }

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


@app.get("/health")
def health():
    return {"status": "ok"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, reload=True)