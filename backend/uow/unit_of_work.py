from sqlmodel import Session
from backend.database import engine
from backend.repositories.producto_repository import ProductoRepository
from backend.repositories.categoria_repository import CategoriaRepository
from backend.repositories.ingrediente_repository import IngredienteRepository
from backend.repositories.usuario_repository import UsuarioRepository
from backend.repositories.rol_repository import RolRepository
from backend.repositories.pedido_repository import PedidoRepository
from backend.repositories.estado_pedido_repository import EstadoPedidoRepository
from backend.repositories.direccion_repository import DireccionRepository
from backend.repositories.unidad_medida_repository import UnidadMedidaRepository
from backend.repositories.movimiento_stock_repository import MovimientoStockRepository
from backend.repositories.pago_repository import PagoRepository


class UnitOfWork:
    def __init__(self, _engine=None):
        self._engine = _engine or engine
        self.session: Session = None
        self.productos: ProductoRepository = None
        self.categorias: CategoriaRepository = None
        self.ingredientes: IngredienteRepository = None
        self.usuarios: UsuarioRepository = None
        self.roles: RolRepository = None
        self.pedidos: PedidoRepository = None
        self.estados_pedido: EstadoPedidoRepository = None
        self.direcciones: DireccionRepository = None
        self.unidades_medida: UnidadMedidaRepository = None
        self.movimientos_stock: MovimientoStockRepository = None
        self.pagos: PagoRepository = None

    def __enter__(self):
        self.session = Session(self._engine, expire_on_commit=False)
        self.productos = ProductoRepository(self.session)
        self.categorias = CategoriaRepository(self.session)
        self.ingredientes = IngredienteRepository(self.session)
        self.usuarios = UsuarioRepository(self.session)
        self.roles = RolRepository(self.session)
        self.pedidos = PedidoRepository(self.session)
        self.estados_pedido = EstadoPedidoRepository(self.session)
        self.direcciones = DireccionRepository(self.session)
        self.unidades_medida = UnidadMedidaRepository(self.session)
        self.movimientos_stock = MovimientoStockRepository(self.session)
        self.pagos = PagoRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()
