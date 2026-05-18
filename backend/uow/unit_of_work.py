from sqlmodel import Session
from backend.database import engine
from backend.repositories.producto_repository import ProductoRepository
from backend.repositories.categoria_repository import CategoriaRepository
from backend.repositories.ingrediente_repository import IngredienteRepository
from backend.repositories.usuario_repository import UsuarioRepository
from backend.repositories.rol_repository import RolRepository
from backend.repositories.pedido_repository import PedidoRepository
from backend.repositories.estado_pedido_repository import EstadoPedidoRepository

class UnitOfWork:
    def __init__(self):
        self.session: Session = None
        self.productos: ProductoRepository = None
        self.categorias: CategoriaRepository = None
        self.ingredientes: IngredienteRepository = None
        self.usuarios: UsuarioRepository = None
        self.roles: RolRepository = None
        self.pedidos: PedidoRepository = None
        self.estados_pedido: EstadoPedidoRepository = None

    def __enter__(self):
        self.session = Session(engine, expire_on_commit=False)
        self.productos = ProductoRepository(self.session)
        self.categorias = CategoriaRepository(self.session)
        self.ingredientes = IngredienteRepository(self.session)
        self.usuarios = UsuarioRepository(self.session)
        self.roles = RolRepository(self.session)
        self.pedidos = PedidoRepository(self.session)
        self.estados_pedido = EstadoPedidoRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()
