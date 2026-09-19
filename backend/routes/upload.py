from fastapi import APIRouter, UploadFile, File
from storage import save_upload

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    result = await save_upload(file)
    # Devolvemos solo lo que el frontend necesita
    return {
        "file_id": result["file_id"],
        "filename": result["filename"],
        "content_type": result["content_type"],
    }