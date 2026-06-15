import hashlib
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlmodel import select
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
    # Verificar si el email ya existe
    existing_user = uow.usuarios.get_by_email(data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Hashear password
    hashed_password = get_password_hash(data.password)
    
    # Crear usuario
    usuario = Usuario(
        nombre=data.nombre,
        apellido=data.apellido,
        email=data.email,
        celular=data.celular,
        password_hash=hashed_password
    )
    
    uow.usuarios.add(usuario)
    uow.session.flush()
    uow.session.refresh(usuario)
    return usuario


def actualizar_usuario(uow: UnitOfWork, usuario: Usuario, data: UsuarioUpdate) -> Usuario:
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(usuario, k, v)
    uow.session.flush()
    uow.session.refresh(usuario)
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
    uow.session.add(rt)
    uow.session.flush()
    return rt


def validar_refresh_token(uow: UnitOfWork, token_str: str) -> Usuario:
    try:
        import jwt as pyjwt
        payload = pyjwt.decode(token_str, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Refresh token inválido")

        token_hash = hashlib.sha256(token_str.encode()).hexdigest()
        stored = uow.session.exec(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        ).first()

        if not stored:
            raise HTTPException(status_code=401, detail="Refresh token no encontrado")

        if stored.revoked_at is not None:
            all_active = uow.session.exec(
                select(RefreshToken).where(
                    RefreshToken.usuario_id == stored.usuario_id,
                    RefreshToken.revoked_at.is_(None),
                )
            ).all()
            for t in all_active:
                t.revoked_at = datetime.now(timezone.utc)
            uow.session.flush()
            raise HTTPException(
                status_code=401,
                detail="Refresh token reutilizado — todas las sesiones fueron invalidadas"
            )

        if stored.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Refresh token expirado")

        stored.revoked_at = datetime.now(timezone.utc)
        uow.session.flush()

        return uow.usuarios.get_by_id(int(payload["sub"]))
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token inválido")


def revocar_refresh_token(uow: UnitOfWork, token_str: str):
    token_hash = hashlib.sha256(token_str.encode()).hexdigest()
    stored = uow.session.exec(
        select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    ).first()
    if stored:
        stored.revoked_at = datetime.now(timezone.utc)
        uow.session.add(stored)
        uow.session.flush()
