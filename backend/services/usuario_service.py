from fastapi import HTTPException, status
from passlib.context import CryptContext
from backend.models.usuario import Usuario
from backend.schemas.usuario import UsuarioCreate, UsuarioUpdate
from backend.uow.unit_of_work import UnitOfWork

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
    print(f"DEBUG LOGIN: email='{email}', password='{password}'")
    usuario = uow.usuarios.get_by_email(email)
    print(f"DEBUG LOGIN: usuario encontrado={usuario is not None}")
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    is_valid = verify_password(password, usuario.password_hash)
    print(f"DEBUG LOGIN: password verificado={is_valid}")
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    return usuario
