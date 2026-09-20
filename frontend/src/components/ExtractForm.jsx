import { useState } from "react";

import { validateInvoice } from "../api";


function createFormData(invoice) {
  return {
    provider: invoice.provider ?? "",
    invoice_date: invoice.invoice_date ?? "",
    total_amount: invoice.total_amount ?? "",
    tax_amount: invoice.tax_amount ?? "",
    currency: invoice.currency ?? "EUR",
  };
}


export default function ExtractForm({ invoice, onValidated }) {
  const [formData, setFormData] = useState(() => createFormData(invoice));
  const [isValidating, setIsValidating] = useState(false);
  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((currentData) => ({
      ...currentData,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setIsValidating(true);
      setError("");

      const result = await validateInvoice(formData);
      onValidated(result.data);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsValidating(false);
    }
  }

  return (
    <section>
      <h2>Revisar datos extraídos</h2>

      <p>
        Comprueba los valores detectados y corrige cualquier dato antes de
        validar la factura.
      </p>

      <form onSubmit={handleSubmit}>
        <label htmlFor="provider">Proveedor</label>
        <input
          id="provider"
          name="provider"
          type="text"
          value={formData.provider}
          onChange={handleChange}
          disabled={isValidating}
          required
        />

        <label htmlFor="invoice_date">Fecha de emisión</label>
        <input
          id="invoice_date"
          name="invoice_date"
          type="date"
          value={formData.invoice_date}
          onChange={handleChange}
          disabled={isValidating}
          required
        />

        <label htmlFor="total_amount">Importe total</label>
        <input
          id="total_amount"
          name="total_amount"
          type="number"
          value={formData.total_amount}
          onChange={handleChange}
          disabled={isValidating}
          min="0.01"
          step="0.01"
          required
        />

        <label htmlFor="tax_amount">Impuestos</label>
        <input
          id="tax_amount"
          name="tax_amount"
          type="number"
          value={formData.tax_amount}
          onChange={handleChange}
          disabled={isValidating}
          min="0"
          step="0.01"
          required
        />

        <label htmlFor="currency">Moneda</label>
        <select
          id="currency"
          name="currency"
          value={formData.currency}
          onChange={handleChange}
          disabled={isValidating}
        >
          <option value="EUR">EUR</option>
        </select>

        {error && (
          <p className="error-message" role="alert">
            {error}
          </p>
        )}

        <button type="submit" disabled={isValidating}>
          {isValidating ? "Validando..." : "Validar factura"}
        </button>
      </form>
    </section>
  );
}