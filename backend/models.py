from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class InvoiceDraft(BaseModel):
    """
    Resultado preliminar de la extracción.

    Todos los campos principales son opcionales porque una regla de extracción
    puede no haber encontrado un dato.
    """

    provider: str | None = None
    invoice_date: date | None = None
    total_amount: Decimal | None = Field(default=None, gt=0)
    tax_amount: Decimal | None = Field(default=None, ge=0)
    currency: Literal["EUR"] = "EUR"
    raw_text: str | None = None


class InvoiceValidated(BaseModel):
    """
    Factura corregida y validada. Lista para exportar.
    """

    provider: str = Field(max_length=200)
    invoice_date: date
    total_amount: Decimal = Field(gt=0)
    tax_amount: Decimal = Field(ge=0)
    currency: Literal["EUR"] = "EUR"

    @field_validator("provider")
    @classmethod
    def provider_cannot_be_blank(cls, value: str) -> str:
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("El proveedor no puede estar vacío.")

        return normalized_value

    @field_validator("invoice_date")
    @classmethod
    def invoice_date_cannot_be_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("La fecha de la factura no puede estar en el futuro.")

        return value

    @model_validator(mode="after")
    def tax_cannot_exceed_total(self):
        if self.tax_amount > self.total_amount:
            raise ValueError(
                "Los impuestos no pueden ser superiores al importe total."
            )

        return self