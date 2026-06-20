import hashlib
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext
from backend.models.usuario import Usuario
from backend.models.refresh_token import RefreshToken
from backend.schemas.usuario import UsuarioCreate, UsuarioUpdate
from backend.uow.unit_of_work import UnitOfWork
from backend.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def registrar_usuario(uow: UnitOfWork, data: UsuarioCreate) -> Usuario:
    existing_user = uow.usuarios.get_by_email(data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    hashed_password = get_password_hash(data.password)
    
    usuario = Usuario(
        nombre=data.nombre,
        apellido=data.apellido,
        email=data.email,
        celular=data.celular,
        password_hash=hashed_password
    )
    
    uow.usuarios.add(usuario)
    uow.flush()
    uow.usuarios.refresh(usuario)
    return usuario


def actualizar_usuario(uow: UnitOfWork, usuario: Usuario, data: UsuarioUpdate) -> Usuario:
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(usuario, k, v)
    uow.usuarios.add(usuario)
    uow.flush()
    uow.usuarios.refresh(usuario)
    return usuario


def autenticar_usuario(uow: UnitOfWork, email: str, password: str) -> Usuario:
    usuario = uow.usuarios.get_by_email(email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    is_valid = verify_password(password, usuario.password_hash)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    return usuario


def guardar_refresh_token(uow: UnitOfWork, usuario_id: int, token_str: str) -> RefreshToken:
    token_hash = hashlib.sha256(token_str.encode()).hexdigest()
    expires = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    rt = RefreshToken(
        token_hash=token_hash,
        usuario_id=usuario_id,
        expires_at=expires,
    )
    uow.refresh_tokens.add(rt)
    uow.flush()
    return rt


def validar_refresh_token(uow: UnitOfWork, token_str: str) -> Usuario:
    try:
        import jwt as pyjwt
        payload = pyjwt.decode(token_str, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Refresh token inválido")

        token_hash = hashlib.sha256(token_str.encode()).hexdigest()
        stored = uow.refresh_tokens.get_by_hash(token_hash)

        if not stored:
            raise HTTPException(status_code=401, detail="Refresh token no encontrado")

        if stored.revoked_at is not None:
            all_active = uow.refresh_tokens.get_active_by_user(stored.usuario_id)
            for t in all_active:
                t.revoked_at = datetime.now(timezone.utc)
                uow.refresh_tokens.add(t)
            uow.flush()
            raise HTTPException(
                status_code=401,
                detail="Refresh token reutilizado — todas las sesiones fueron invalidadas"
            )

        if stored.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Refresh token expirado")

        stored.revoked_at = datetime.now(timezone.utc)
        uow.refresh_tokens.add(stored)
        uow.flush()

        return uow.usuarios.get_by_id(int(payload["sub"]))
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token inválido")


def revocar_refresh_token(uow: UnitOfWork, token_str: str):
    token_hash = hashlib.sha256(token_str.encode()).hexdigest()
    stored = uow.refresh_tokens.get_by_hash(token_hash)
    if stored:
        stored.revoked_at = datetime.now(timezone.utc)
        uow.refresh_tokens.add(stored)
        uow.flush()
