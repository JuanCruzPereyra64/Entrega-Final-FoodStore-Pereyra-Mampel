from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import uuid
from pathlib import Path

router = APIRouter()

# Carpeta de destino (frontend/store/public/img)
UPLOAD_DIR = Path(__file__).parent.parent.parent / "frontend" / "store" / "public" / "img"

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")
        
    # Crear directorio si no existe
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Generar un nombre único para evitar colisiones
    file_ext = file.filename.split(".")[-1]
    new_filename = f"{uuid.uuid4().hex[:10]}.{file_ext}"
    
    file_path = UPLOAD_DIR / new_filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {str(e)}")
    finally:
        file.file.close()
        
    return {"url": f"/img/{new_filename}"}
