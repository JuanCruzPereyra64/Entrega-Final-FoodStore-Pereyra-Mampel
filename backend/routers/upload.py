from fastapi import APIRouter, UploadFile, File, Depends
from backend.schemas.cloudinary import CloudinaryResponse
from backend.services import upload_service
from backend.models.usuario import Usuario
from backend.api.deps import check_role

router = APIRouter(prefix="/api/v1/uploads", tags=["Uploads"])


@router.post("/imagen", response_model=CloudinaryResponse, status_code=201)
def upload_imagen(
    file: UploadFile = File(...),
    current_user: Usuario = Depends(check_role(["ADMIN"]))
):
    return CloudinaryResponse(**upload_service.upload_to_cloudinary(file, "foodstore/productos"))


@router.delete("/imagen/{public_id}", status_code=204)
def delete_imagen(
    public_id: str,
    current_user: Usuario = Depends(check_role(["ADMIN"]))
):
    upload_service.destroy_from_cloudinary(public_id)
