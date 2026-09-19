from fastapi import APIRouter

from extractor import extract_text_from_pdf
from storage import get_file_path


router = APIRouter()


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