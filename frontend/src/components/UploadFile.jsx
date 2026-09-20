import { useState } from "react";

import { extractFields, uploadFile } from "../api.js";

export default function UploadFile({ onExtracted }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  function handleFileChange(event) {
    const file = event.target.files?.[0] ?? null;

    setSelectedFile(file);
    setError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!selectedFile) {
      setError("Selecciona un PDF, PNG o JPG antes de continuar.");
      return;
    }

    try {
      setIsLoading(true);
      setError("");

      const uploadResult = await uploadFile(selectedFile);
      const extractionResult = await extractFields(uploadResult.file_id);

      onExtracted({
        fileId: uploadResult.file_id,
        filename: uploadResult.filename,
        data: extractionResult.data,
      });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section>
      <h2>Analizar documento</h2>

      <p>
        Sube una factura en PDF, PNG o JPG. El sistema propondrá proveedor,
        fecha, total e impuestos para que los revises.
      </p>

      <form onSubmit={handleSubmit}>
        <label htmlFor="document-file">Archivo de factura</label>

        <input
          id="document-file"
          type="file"
          accept=".pdf,.png,.jpg,.jpeg,application/pdf,image/png,image/jpeg"
          onChange={handleFileChange}
          disabled={isLoading}
        />

        {selectedFile && (
          <p>
            Archivo seleccionado: <strong>{selectedFile.name}</strong>
          </p>
        )}

        {error && (
          <p role="alert">
            {error}
          </p>
        )}

        <button type="submit" disabled={isLoading}>
          {isLoading ? "Analizando documento..." : "Analizar documento"}
        </button>
      </form>
    </section>
  );
}