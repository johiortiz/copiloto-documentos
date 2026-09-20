from fastapi import APIRouter, HTTPException

from extractor import extract_text_from_pdf, extract_invoice_fields
from storage import get_file_path
from models import InvoiceDraft

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

@router.post("/extract-fields/{file_id}")
def extract_fields(file_id: str):
    """
    Extrae un borrador de factura a partir de un PDF ya subido.
    """
    file_path = get_file_path(file_id)

    if file_path.suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=422,
            detail="La extracción de campos de imágenes todavía no está implementada."
        )

    text = extract_text_from_pdf(file_path)
    extracted_fields = extract_invoice_fields(text)

    draft = InvoiceDraft(
        **extracted_fields,
        raw_text=text,
    )

    return {
        "file_id": file_id,
        "data": draft,
    }