from extractor import normalize_text, parse_euro_amount

from extractor import (
    find_invoice_date,
    normalize_text,
    parse_euro_amount,
)

from extractor import (
    find_invoice_date,
    find_total_amount,
    normalize_text,
    parse_euro_amount,
)

from extractor import (
    find_invoice_date,
    find_tax_amount,
    find_total_amount,
    normalize_text,
    parse_euro_amount,
)

raw_text = """
Impuestos
10,76 €

Total
1.234,56 €
"""

invoice_text = """
Endesa Energía, S.A. Unipersonal.
DATOS DE LA FACTURA

Fecha emisión factura:
06/02/2025

Periodo de facturación: del 31/12/2024 a 31/01/2025
"""

total_text = """
Potencia 24,57 €
Energía 13,53 €
Impuestos 10,76 €
Total
50,65 €
"""

tax_text = """
21,24% Impuestos
Potencia 24,57 €
Impuestos
10,76 €
Total
50,65 €
"""



print(normalize_text(raw_text))
print(parse_euro_amount("10,76 €"))
print(parse_euro_amount("1.234,56 €"))
print(find_invoice_date(invoice_text))
print(find_invoice_date("Fecha emisión factura: 99/99/2025"))
print(find_invoice_date("Fecha de cargo: 13/02/2025"))
print(find_total_amount(total_text))
print(find_total_amount("Importe total: 1.234,56 EUR"))
print(find_total_amount("No hay ningún importe final en este texto"))
print(find_tax_amount(tax_text))
print(find_tax_amount("Total impuestos: 1.234,56 EUR"))
print(find_tax_amount("El IVA aplicable es del 21 %"))
print(find_tax_amount("No hay información fiscal disponible"))