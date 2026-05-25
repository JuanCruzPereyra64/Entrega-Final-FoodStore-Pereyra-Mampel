from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from backend.models.producto import Producto, ProductoCategoria
from backend.repositories.base_repository import BaseRepository

class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session):
        super().__init__(Producto, session)

    def get_all(self, categoria_id: Optional[int] = None, offset: int = 0, limit: int = 100) -> list[Producto]:
        statement = (
            select(Producto)
            .options(selectinload(Producto.ingredientes), selectinload(Producto.categorias))
        )
        
        if categoria_id:
            statement = statement.join(ProductoCategoria).where(ProductoCategoria.categoria_id == categoria_id)
            
        statement = statement.offset(offset).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        statement = (
            select(Producto)
            .where(Producto.id == producto_id)
            .options(selectinload(Producto.ingredientes), selectinload(Producto.categorias))
        )
        return self.session.exec(statement).first()
