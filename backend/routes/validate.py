from fastapi import APIRouter

from models import InvoiceValidated


router = APIRouter()


@router.post("/validate-invoice")
def validate_invoice(invoice: InvoiceValidated):
    """
    Recibe una factura corregida por el usuario.

    FastAPI y Pydantic validan el body automáticamente antes de entrar
    en esta función.
    """
    return {
        "valid": True,
        "data": invoice,
    }