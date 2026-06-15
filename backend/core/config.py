import json
from typing import Optional
import cloudinary
import mercadopago
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./foodstore.db"
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    cors_origins: str = '["http://localhost:5173", "http://localhost:5174"]'

    mp_access_token: str = ""
    mp_public_key: str = ""
    mp_notification_url: str = ""

    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return json.loads(self.cors_origins)

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()

mp_sdk: Optional[mercadopago.SDK] = None
if settings.mp_access_token:
    mp_sdk = mercadopago.SDK(settings.mp_access_token)

if settings.cloudinary_cloud_name:
    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret
    )
