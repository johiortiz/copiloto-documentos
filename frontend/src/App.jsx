import { useState } from "react";

import ExportCSV from "./components/ExportCSV";
import ExtractForm from "./components/ExtractForm";
import UploadFile from "./components/UploadFile";


export default function App() {
  const [extractedInvoice, setExtractedInvoice] = useState(null);
  const [validatedInvoice, setValidatedInvoice] = useState(null);

  function handleExtracted(result) {
    setExtractedInvoice(result);
    setValidatedInvoice(null);
  }

  function handleValidated(invoice) {
    setValidatedInvoice(invoice);
  }

  return (
    <main>
      <header>
        <p className="eyebrow">MVP · Document Intelligence</p>
        <h1>Copiloto de documentos</h1>
        <p className="intro">
          Sube una factura, revisa los datos extraídos y exporta un CSV
          validado.
        </p>
      </header>

      <UploadFile onExtracted={handleExtracted} />

      {extractedInvoice && (
        <ExtractForm
          key={extractedInvoice.fileId}
          invoice={extractedInvoice.data}
          onValidated={handleValidated}
        />
      )}

      {validatedInvoice && (
        <>
          <section className="success-card">
            <h2>Factura validada</h2>
            <p>
              Los datos son coherentes y ya están listos para exportarse a CSV.
            </p>
          </section>
          <ExportCSV invoice={validatedInvoice} />
        </>
  )}
      </main>
    );
}