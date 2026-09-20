import { useState } from "react";

import { exportCsv } from "../api";


export default function ExportCSV({ invoice }) {
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState("");

  async function handleExport() {
    try {
      setIsExporting(true);
      setError("");

      const csvBlob = await exportCsv(invoice);

      const downloadUrl = URL.createObjectURL(csvBlob);
      const link = document.createElement("a");

      link.href = downloadUrl;
      link.download = "invoice.csv";

      document.body.appendChild(link);
      link.click();
      link.remove();

      URL.revokeObjectURL(downloadUrl);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsExporting(false);
    }
  }

  return (
    <section>
      <h2>Exportar CSV</h2>

      <p>
        La factura está validada. Puedes descargar los datos en formato CSV.
      </p>

      {error && (
        <p className="error-message" role="alert">
          {error}
        </p>
      )}

      <button type="button" onClick={handleExport} disabled={isExporting}>
        {isExporting ? "Preparando CSV..." : "Exportar CSV"}
      </button>
    </section>
  );
}