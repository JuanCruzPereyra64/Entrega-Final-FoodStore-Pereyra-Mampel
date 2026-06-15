import io
from fastapi import UploadFile, HTTPException

ALLOWED_MIME = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
}
MAX_SIZE = 5 * 1024 * 1024


def validate_image(file: UploadFile):
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no soportado. Permitidos: {', '.join(ALLOWED_MIME.values())}"
        )

    contents = file.file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail="La imagen supera los 5 MB permitidos"
        )
    file.file.seek(0)
    return contents


def upload_to_cloudinary(file: UploadFile, folder: str = "foodstore/productos") -> dict:
    contents = validate_image(file)
    import cloudinary.uploader
    result = cloudinary.uploader.upload(
        contents,
        folder=folder,
        overwrite=False,
        unique_filename=True,
        resource_type="image"
    )
    return {
        "secure_url": result["secure_url"],
        "public_id": result["public_id"],
        "width": result["width"],
        "height": result["height"],
        "format": result["format"],
        "resource_type": result["resource_type"],
    }


def destroy_from_cloudinary(public_id: str):
    import cloudinary.uploader
    result = cloudinary.uploader.destroy(public_id)
    if result.get("result") != "ok":
        raise HTTPException(status_code=400, detail=f"No se pudo eliminar la imagen: {result.get('result')}")
