import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, select
from sqlalchemy.pool import StaticPool
from passlib.context import CryptContext
from backend.database import get_uow
from backend.main import app
from backend.models.rol import Rol
from backend.models.estado_pedido import EstadoPedido
from backend.models.forma_pago import FormaPago
from backend.models.usuario import Usuario
from backend.models.usuario_rol import UsuarioRol
from backend.models.categoria import Categoria
from backend.models.ingrediente import Ingrediente
from backend.models.producto import Producto, ProductoCategoria, ProductoIngrediente
from backend.models.unidad_medida import UnidadMedida
from backend.uow.unit_of_work import UnitOfWork

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
test_engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)


def get_test_uow():
    return UnitOfWork(_engine=test_engine)


def seed_test_db():
    with Session(test_engine) as session:
        roles = ["ADMIN", "STOCK", "PEDIDOS", "CLIENT"]
        for r_name in roles:
            if not session.exec(select(Rol).where(Rol.nombre == r_name)).first():
                session.add(Rol(nombre=r_name, descripcion=f"Rol {r_name}"))

        estados = [
            ("PENDIENTE", 1, False), ("CONFIRMADO", 2, False),
            ("EN_PREP", 3, False), ("ENTREGADO", 4, True), ("CANCELADO", 5, True),
        ]
        for codigo, orden, terminal in estados:
            if not session.exec(select(EstadoPedido).where(EstadoPedido.codigo == codigo)).first():
                session.add(EstadoPedido(codigo=codigo, descripcion=codigo, orden=orden, es_terminal=terminal))

        for codigo in ["MERCADOPAGO", "EFECTIVO", "TRANSFERENCIA"]:
            if not session.exec(select(FormaPago).where(FormaPago.codigo == codigo)).first():
                session.add(FormaPago(codigo=codigo, descripcion=codigo))

        session.commit()

        admin_rol = session.exec(select(Rol).where(Rol.nombre == "ADMIN")).first()
        client_rol = session.exec(select(Rol).where(Rol.nombre == "CLIENT")).first()

        admin = session.exec(select(Usuario).where(Usuario.email == "admin@foodstore.com")).first()
        if not admin:
            admin = Usuario(nombre="Admin", apellido="Test", email="admin@foodstore.com", password_hash=pwd_context.hash("Admin1234!"))
            session.add(admin)
            session.flush()
            session.add(UsuarioRol(usuario_id=admin.id, rol_id=admin_rol.id))

        client = session.exec(select(Usuario).where(Usuario.email == "client@test.com")).first()
        if not client:
            client = Usuario(nombre="Client", apellido="Test", email="client@test.com", password_hash=pwd_context.hash("Client1234"))
            session.add(client)
            session.flush()
            session.add(UsuarioRol(usuario_id=client.id, rol_id=client_rol.id))

        cat = session.exec(select(Categoria).where(Categoria.nombre == "Bebidas")).first()
        if not cat:
            cat = Categoria(nombre="Bebidas", descripcion="Bebidas")
            session.add(cat)
            session.flush()

        um = session.exec(select(UnidadMedida).where(UnidadMedida.nombre == "ud")).first()
        if not um:
            um = UnidadMedida(nombre="ud", simbolo="ud", tipo="contable")
            session.add(um)
            session.flush()

        ing = session.exec(select(Ingrediente).where(Ingrediente.nombre == "Ingrediente Test")).first()
        if not ing:
            ing = Ingrediente(nombre="Ingrediente Test", es_alergeno=False, unidad_medida_id=um.id, stock_cantidad=1000)
            session.add(ing)
            session.flush()

        prod = session.exec(select(Producto).where(Producto.nombre == "Producto Test")).first()
        if not prod:
            prod = Producto(nombre="Producto Test", descripcion="Test", precio_base=100, stock_cantidad=50, disponible=True)
            session.add(prod)
            session.flush()
            session.add(ProductoCategoria(producto_id=prod.id, categoria_id=cat.id, es_principal=True))
            session.add(ProductoIngrediente(producto_id=prod.id, ingrediente_id=ing.id, unidad_medida_id=um.id, es_removible=True, es_opcional=False, cantidad=1))

        prod2 = session.exec(select(Producto).where(Producto.nombre == "Producto Test 2")).first()
        if not prod2:
            prod2 = Producto(nombre="Producto Test 2", descripcion="Test 2", precio_base=200, stock_cantidad=30, disponible=True)
            session.add(prod2)
            session.flush()
            session.add(ProductoCategoria(producto_id=prod2.id, categoria_id=cat.id, es_principal=True))
            session.add(ProductoIngrediente(producto_id=prod2.id, ingrediente_id=ing.id, unidad_medida_id=um.id, es_removible=True, es_opcional=False, cantidad=1))

        session.commit()
        return {"admin_id": admin.id, "client_id": client.id}


@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(test_engine)
    seed_test_db()
    yield
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_uow] = lambda: get_test_uow()
    app.state.limiter.enabled = False
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    app.state.limiter.enabled = True


@pytest.fixture
def admin_headers(client: TestClient):
    res = client.post("/api/v1/auth/login", json={"email": "admin@foodstore.com", "password": "Admin1234!"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def client_headers(client: TestClient):
    res = client.post("/api/v1/auth/login", json={"email": "client@test.com", "password": "Client1234"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
