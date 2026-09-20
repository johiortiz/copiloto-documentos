const API_URL = "http://127.0.0.1:8000/api";

async function getErrorMessage(response) {
  try {
    const body = await response.json();

    if (Array.isArray(body.detail)) {
      return body.detail
        .map((error) => error.msg)
        .join(" ");
    }

    return body.detail || "Ha ocurrido un error inesperado.";
  } catch {
    return "Ha ocurrido un error inesperado.";
  }
}

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await getErrorMessage(response));
  }

  return response.json();
}

export async function extractFields(fileId) {
  const response = await fetch(`${API_URL}/extract-fields/${fileId}`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error(await getErrorMessage(response));
  }

  return response.json();
}

export async function validateInvoice(invoice) {
  const response = await fetch(`${API_URL}/validate-invoice`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(invoice),
  });

  if (!response.ok) {
    throw new Error(await getErrorMessage(response));
  }

  return response.json();
}

export async function exportCsv(invoice) {
  const response = await fetch(`${API_URL}/export-csv`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(invoice),
  });

  if (!response.ok) {
    throw new Error(await getErrorMessage(response));
  }

  return response.blob();
}