from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re

from fastapi import HTTPException
from pypdf import PdfReader

MONEY_PATTERN = r"(\d{1,3}(?:\.\d{3})*(?:,\d{2})|\d+(?:\.\d{2})?)"

def extract_text_from_pdf(file_path: Path) -> str:
    """
    Extrae y concatena el texto de todas las páginas de un PDF digital.
    """

    try:
        reader = PdfReader(str(file_path))
    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail="No se pudo abrir el PDF. Puede estar corrupto o protegido."
        ) from error

    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        pages_text.append(page_text)

    full_text = "\n".join(pages_text).strip()

    if not full_text:
        raise HTTPException(
            status_code=422,
            detail=(
                "No se encontró texto en el PDF. "
                "Probablemente es un PDF escaneado y necesitará OCR."
            )
        )

    return full_text

def normalize_text(text: str) -> str:
    """
    Convierte secuencias de espacios, saltos de línea y tabulaciones
    en un único espacio.
    """
    return re.sub(r"\s+", " ", text).strip()

def parse_euro_amount(value: str) -> float | None:
    """
    Convierte formatos europeos de dinero a float.

    Ejemplos:
    '50,65'    -> 50.65
    '1.234,56' -> 1234.56
    '50.65'    -> 50.65
    """
    cleaned = value.strip().replace("€", "").replace("EUR", "").strip()

    if "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")

    try:
        return float(Decimal(cleaned))
    except InvalidOperation:
        return None

def find_invoice_date(text: str) -> str | None:
    """
    Busca la fecha de emisión de la factura y la devuelve en ISO:
    YYYY-MM-DD.

    Devuelve None si no aparece una fecha válida con la etiqueta esperada.
    """
    normalized_text = normalize_text(text)

    pattern = (
        r"fecha\s+(?:de\s+)?emisi[oó]n\s+(?:de\s+la\s+)?factura"
        r"\s*:\s*"
        r"(\d{1,2}[/-]\d{1,2}[/-]\d{4})"
    )

    match = re.search(pattern, normalized_text, flags=re.IGNORECASE)

    if not match:
        return None

    raw_date = match.group(1).replace("-", "/")

    try:
        return datetime.strptime(raw_date, "%d/%m/%Y").date().isoformat()
    except ValueError:
        return None

def find_total_amount(text: str) -> float | None:
    """
    Busca el importe total de una factura.

    Usa etiquetas ordenadas por confianza y devuelve None si no encuentra
    un importe asociado a ellas.
    """
    normalized_text = normalize_text(text)

    labels = [
        r"importe\s+total",
        r"total\s+a\s+pagar",
        r"total",
    ]

    for label in labels:
        pattern = rf"\b{label}\b\s*:?\s*{MONEY_PATTERN}\s*(?:€|eur|euros?)"

        match = re.search(pattern, normalized_text, flags=re.IGNORECASE)

        if match:
            return parse_euro_amount(match.group(1))

    return None

def find_tax_amount(text: str) -> float | None:
    """
    Busca el importe total de impuestos de una factura.

    Devuelve el importe asociado a etiquetas como "Impuestos" o
    "Total impuestos". No acepta porcentajes como 21,24 %.
    """
    normalized_text = normalize_text(text)

    labels = [
        r"total\s+impuestos",
        r"impuestos",
    ]

    for label in labels:
        pattern = rf"\b{label}\b\s*:?\s*{MONEY_PATTERN}\s*(?:€|eur|euros?)"

        match = re.search(pattern, normalized_text, flags=re.IGNORECASE)

        if match:
            return parse_euro_amount(match.group(1))

    return None

def find_provider(text: str) -> str | None:
    """
    Busca una posible razón social del emisor de la factura.

    Primera versión: identifica empresas españolas con formas jurídicas
    comunes, como S.A., S.L. o variantes Unipersonal.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    provider_pattern = re.compile(
        r"^(.+?\bS\.\s*(?:A|L)\.?(?:\s+Unipersonal)?)",
        flags=re.IGNORECASE,
    )

    for line in lines[:40]:
        match = provider_pattern.search(line)

        if match:
            return match.group(1).strip()

    return None

def extract_invoice_fields(text: str) -> dict:
    """
    Extrae los campos principales de una factura a partir de su texto.

    Los valores pueden ser None cuando no se han podido detectar.
    """
    return {
        "provider": find_provider(text),
        "invoice_date": find_invoice_date(text),
        "total_amount": find_total_amount(text),
        "tax_amount": find_tax_amount(text),
        "currency": "EUR",
    }