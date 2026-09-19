CORS_ORIGINS = [
    "http://localhost:5173",  # Vite dev
    "http://127.0.0.1:5173",
]

MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
TEMP_DIR = "/tmp/copiloto_docs"  # o usa tempfile.gettempdir() / una carpeta en el proyecto