from datetime import date
from decimal import Decimal

from pydantic import ValidationError

from models import InvoiceDraft, InvoiceValidated


valid_invoice = InvoiceValidated(
    provider="  Endesa Energía, S.A. Unipersonal  ",
    invoice_date=date(2025, 2, 6),
    total_amount=Decimal("50.65"),
    tax_amount=Decimal("10.76"),
)

print(valid_invoice.model_dump())
print(valid_invoice.provider)

draft_without_provider = InvoiceDraft(
    invoice_date="2025-02-06",
    total_amount="50.65",
    tax_amount="10.76",
)

print(draft_without_provider.model_dump())


try:
    InvoiceValidated(
        provider="   ",
        invoice_date="2025-02-06",
        total_amount="50.65",
        tax_amount="10.76",
    )
except ValidationError as error:
    print(error.errors())

try:
    InvoiceValidated(
        provider="Endesa Energía, S.A. Unipersonal",
        invoice_date="2025-02-06",
        total_amount="50.65",
        tax_amount="70.00",
    )
except ValidationError as error:
    print(error.errors())

try:
    InvoiceValidated(
        provider="Endesa Energía, S.A. Unipersonal",
        invoice_date="2099-01-01",
        total_amount="50.65",
        tax_amount="10.76",
    )
except ValidationError as error:
    print(error.errors())

