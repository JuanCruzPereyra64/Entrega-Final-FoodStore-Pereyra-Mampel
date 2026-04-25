from sqlmodel import Session
from backend.database import engine
from backend.repositories.producto_repository import ProductoRepository
from backend.repositories.categoria_repository import CategoriaRepository
from backend.repositories.ingrediente_repository import IngredienteRepository

class UnitOfWork:
    def __init__(self):
        self.session: Session = None
        self.productos: ProductoRepository = None
        self.categorias: CategoriaRepository = None
        self.ingredientes: IngredienteRepository = None

    def __enter__(self):
        self.session = Session(engine)
        self.productos = ProductoRepository(self.session)
        self.categorias = CategoriaRepository(self.session)
        self.ingredientes = IngredienteRepository(self.session)
        return self

    def commit(self):
        self.session.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        self.session.close()
