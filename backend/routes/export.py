import csv
import io

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models import InvoiceValidated


router = APIRouter()


@router.post("/export-csv")
def export_csv(invoice: InvoiceValidated):
    """
    Genera un CSV descargable a partir de una factura validada.
    """
    buffer = io.StringIO()

    writer = csv.DictWriter(
        buffer,
        fieldnames=[
            "provider",
            "invoice_date",
            "total_amount",
            "tax_amount",
            "currency",
        ],
    )

    writer.writeheader()

    writer.writerow(
        {
            "provider": invoice.provider,
            "invoice_date": invoice.invoice_date.isoformat(),
            "total_amount": str(invoice.total_amount),
            "tax_amount": str(invoice.tax_amount),
            "currency": invoice.currency,
        }
    )

    csv_bytes = buffer.getvalue().encode("utf-8-sig")
    buffer.close()

    return StreamingResponse(
        iter([csv_bytes]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": 'attachment; filename="invoice.csv"',
        },
    )