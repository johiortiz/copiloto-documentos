import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException

from config import MAX_UPLOAD_SIZE, TEMP_DIR

ALLOWED_MIMES = {
    "application/pdf": ".pdf",
    "image/png": ".png",
    "image/jpeg": ".jpg",
}

def ensure_temp_dir():
    Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)

def validate_file(file: UploadFile):
    if file.content_type not in ALLOWED_MIMES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo no permitido: {file.content_type}. Solo PDF, PNG, JPG."
        )

async def save_upload(file: UploadFile) -> dict:
    ensure_temp_dir()
    validate_file(file)

    # Leer contenido (en producción usarías stream, pero para MVP está bien)
    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="Archivo demasiado grande (>5MB).")

    file_id = str(uuid.uuid4())
    ext = ALLOWED_MIMES[file.content_type]
    file_path = Path(TEMP_DIR) / f"{file_id}{ext}"

    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "file_id": file_id,
        "filename": file.filename or "unknown",
        "content_type": file.content_type,
        "file_path": str(file_path),
    }

def get_file_path(file_id: str) -> Path:
    # Buscar archivo con cualquier extensión permitida
    for ext in ALLOWED_MIMES.values():
        path = Path(TEMP_DIR) / f"{file_id}{ext}"
        if path.exists():
            return path
    raise HTTPException(status_code=404, detail="Archivo no encontrado.")

def cleanup_file(file_id: str):
    try:
        path = get_file_path(file_id)
        path.unlink(missing_ok=True)
    except HTTPException:
        pass  # Si no existe, no hacer nada