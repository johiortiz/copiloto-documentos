# Copiloto de documentos

Aplicación full-stack para analizar facturas y transformar documentos no estructurados en datos revisables y exportables.

El usuario puede subir una factura en PDF, el sistema extrae texto, identifica campos clave mediante reglas y expresiones regulares, permite corregirlos manualmente, valida las reglas de negocio y descarga un archivo CSV.

## Demo del flujo

```text
Factura PDF
  ↓
Subida de archivo
  ↓
Extracción de texto con pypdf
  ↓
Detección de proveedor, fecha, total e impuestos
  ↓
Revisión manual en React
  ↓
Validación con Pydantic
  ↓
Exportación a CSV
```

## Funcionalidades

- Subida de archivos PDF, PNG y JPG/JPEG.
- Validación de tipo MIME y límite máximo de tamaño de archivo.
- Almacenamiento temporal mediante UUID.
- Extracción de texto de PDFs digitales con `pypdf`.
- Identificación inicial de campos de factura:
  - Proveedor/emisor.
  - Fecha de emisión.
  - Importe total.
  - Impuestos.
  - Moneda.
- Normalización de texto e importes europeos, por ejemplo `1.234,56 €` → `1234.56`.
- Validación de reglas de negocio con Pydantic:
  - El proveedor no puede estar vacío.
  - La fecha de factura no puede estar en el futuro.
  - El total debe ser mayor que cero.
  - Los impuestos no pueden ser negativos.
  - Los impuestos no pueden superar el importe total.
  - La moneda admitida en el MVP es `EUR`.
- Formulario React para corregir los valores extraídos.
- Estados de carga y mensajes de error en la interfaz.
- Exportación de facturas validadas a CSV.

## Capturas y caso de prueba

El proyecto se ha probado con una factura de energía de ejemplo. Para proteger datos personales, no subas ni incluyas facturas reales en el repositorio público.

Ejemplo de datos extraídos:

```json
{
  "provider": "Endesa Energía, S.A. Unipersonal",
  "invoice_date": "2025-02-06",
  "total_amount": "50.65",
  "tax_amount": "10.76",
  "currency": "EUR"
}
```

Ejemplo de CSV exportado:

```csv
provider,invoice_date,total_amount,tax_amount,currency
"Endesa Energía, S.A. Unipersonal",2025-02-06,50.65,10.76,EUR
```

## Arquitectura

```text
copiloto-documentos/
├── backend/
│   ├── config.py                 # Configuración, CORS y directorio temporal
│   ├── extractor.py              # PDF, normalización, regex y heurísticas
│   ├── main.py                   # Aplicación FastAPI y routers
│   ├── models.py                 # Modelos y validadores Pydantic
│   ├── storage.py                # Subida, búsqueda y limpieza de archivos
│   ├── routes/
│   │   ├── upload.py             # POST /api/upload
│   │   ├── extract.py            # Extracción de texto y campos
│   │   ├── validate.py           # POST /api/validate-invoice
│   │   └── export.py             # POST /api/export-csv
│   └── tests/
│       ├── test_manual.py        # Pruebas manuales del extractor
│       └── test_models_manual.py # Pruebas manuales de Pydantic
│
└── frontend/
    ├── src/
    │   ├── api.js                # Cliente HTTP para FastAPI
    │   ├── App.jsx               # Estado principal y composición de la UI
    │   ├── components/
    │   │   ├── UploadFile.jsx    # Selección, subida y extracción
    │   │   ├── ExtractForm.jsx   # Revisión y validación de datos
    │   │   └── ExportCSV.jsx     # Descarga de CSV mediante Blob
    │   └── styles/
    │       └── index.css         # Estilos globales
    └── package.json
```

## Stack tecnológico

### Backend

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic v2
- pypdf
- python-multipart

### Frontend

- React
- Vite
- JavaScript
- CSS

## Requisitos

- Python 3.10 o superior.
- Node.js 20 o superior recomendado.
- npm.

> El MVP actual extrae texto de PDFs digitales. Aunque admite subir PNG y JPG/JPEG, el procesamiento OCR de imágenes todavía no está implementado.

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd copiloto-documentos
```

### 2. Configurar el backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
```

En Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
python -m pip install fastapi uvicorn pydantic python-multipart pypdf pytesseract pillow
```

Inicia el servidor:

```bash
uvicorn main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

Documentación interactiva de FastAPI:

```text
http://127.0.0.1:8000/docs
```

### 3. Configurar el frontend

Abre otra terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite mostrará una URL, normalmente:

```text
http://localhost:5173
```

Abre esa dirección en el navegador.

## Uso

1. Abre el frontend en `http://localhost:5173`.
2. Selecciona una factura PDF digital.
3. Pulsa **Analizar documento**.
4. Revisa proveedor, fecha, total e impuestos.
5. Corrige los datos si fuera necesario.
6. Pulsa **Validar factura**.
7. Si los datos cumplen las reglas, pulsa **Exportar CSV**.

## Endpoints de la API

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/health` | Comprueba que la API está disponible |
| `POST` | `/api/upload` | Sube un PDF, PNG o JPG/JPEG y devuelve un `file_id` |
| `GET` | `/api/extract-text/{file_id}` | Devuelve el texto plano extraído del documento |
| `POST` | `/api/extract-fields/{file_id}` | Devuelve un borrador con los campos detectados |
| `POST` | `/api/validate-invoice` | Valida una factura corregida con Pydantic |
| `POST` | `/api/export-csv` | Devuelve un CSV descargable desde una factura válida |

### Ejemplo: validar una factura

```bash
curl -X POST \
  http://127.0.0.1:8000/api/validate-invoice \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "Empresa de ejemplo, S.L.",
    "invoice_date": "2025-02-06",
    "total_amount": "50.65",
    "tax_amount": "10.76",
    "currency": "EUR"
  }'
```

Respuesta esperada:

```json
{
  "valid": true,
  "data": {
    "provider": "Empresa de ejemplo, S.L.",
    "invoice_date": "2025-02-06",
    "total_amount": "50.65",
    "tax_amount": "10.76",
    "currency": "EUR"
  }
}
```

### Ejemplo: error de negocio

Si `tax_amount` es superior a `total_amount`, la API devuelve `422 Unprocessable Content`:

```json
{
  "detail": [
    {
      "msg": "Value error, Los impuestos no pueden ser superiores al importe total."
    }
  ]
}
```

## Diseño de datos

El proyecto distingue dos modelos:

### `InvoiceDraft`

Representa el resultado inicial del extractor. Sus campos principales pueden ser `null`, porque una factura puede tener un formato que las heurísticas aún no reconocen.

```text
Extractor → InvoiceDraft → Formulario de revisión
```

### `InvoiceValidated`

Representa una factura revisada y válida. Solo este modelo puede usarse para exportar CSV.

```text
Formulario corregido → InvoiceValidated → CSV
```

Esta separación evita rechazar una factura completa solo porque el extractor no detectó un dato y permite la corrección humana.

## Notas de seguridad y privacidad

Las facturas pueden contener información personal, fiscal y bancaria. Antes de desplegar el proyecto o publicar el código:

- No subas facturas reales al repositorio.
- Añade documentos de prueba anonimizados si quieres incluir muestras.
- Mantén `venv/`, `node_modules/`, archivos CSV y variables de entorno fuera de Git.
- No devuelvas `raw_text` al navegador en producción salvo que sea estrictamente necesario.
- Implementa limpieza automática de los archivos temporales.
- Valida el contenido real de los archivos, no solo el MIME type enviado por el navegador.
- Añade autenticación y control de acceso antes de procesar documentos de terceros.

## Limitaciones actuales

- La extracción está optimizada inicialmente para PDFs digitales con texto seleccionable.
- La subida de PNG/JPG/JPEG está permitida, pero el flujo OCR todavía no está integrado.
- Las heurísticas de proveedor se centran en formas jurídicas españolas frecuentes.
- No hay persistencia en base de datos ni historial de documentos.
- No hay autenticación de usuarios.
- El almacenamiento de archivos es temporal.
- `raw_text` se devuelve durante desarrollo para facilitar depuración.

## Próximas mejoras

- [ ] Reemplazar pruebas manuales por `pytest` con `assert`.
- [ ] Añadir pruebas de integración para los endpoints FastAPI.
- [ ] Implementar OCR para PNG, JPG y PDFs escaneados con Tesseract.
- [ ] Preprocesar imágenes antes del OCR: escala de grises, contraste y rotación.
- [ ] Mostrar errores de Pydantic junto a cada campo del formulario.
- [ ] Añadir nivel de confianza y fragmento de origen para cada valor extraído.
- [ ] Soportar más monedas, idiomas y formatos de factura.
- [ ] Persistir facturas validadas en SQLite o PostgreSQL.
- [ ] Añadir autenticación de usuarios.
- [ ] Añadir Docker, variables de entorno y CI/CD.
- [ ] Desplegar frontend y backend.

## Aprendizajes del proyecto

Este proyecto practica:

- Arquitectura frontend/backend.
- APIs REST con FastAPI.
- Gestión temporal de archivos.
- Procesamiento de PDFs.
- Datos no estructurados y expresiones regulares.
- Normalización de texto y formatos monetarios europeos.
- Validación de datos y reglas de negocio con Pydantic.
- Precisión monetaria con `Decimal`.
- Formularios controlados en React.
- Comunicación HTTP con `fetch`, `FormData` y `Blob`.
- Descarga de archivos desde el navegador.
- Diseño de UX con revisión humana en el flujo de extracción.

## Autor

**Johi Ortiz Vallejos**

Proyecto de portfolio orientado a desarrollo full-stack, automatización documental y extracción de datos.