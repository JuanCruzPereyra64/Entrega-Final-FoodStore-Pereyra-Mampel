from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from backend.models.producto import Producto, ProductoIngrediente, ProductoCategoria
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

    def count_all(self, categoria_id: Optional[int] = None) -> int:
        from sqlalchemy import func
        query = select(func.count(Producto.id))
        if categoria_id:
            query = query.join(ProductoCategoria).where(ProductoCategoria.categoria_id == categoria_id)
        return self.session.exec(query).one()

    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        statement = (
            select(Producto)
            .where(Producto.id == producto_id)
            .options(selectinload(Producto.ingredientes), selectinload(Producto.categorias))
        )
        return self.session.exec(statement).first()

    def get_ingrediente_links(self, producto_id: int) -> list[ProductoIngrediente]:
        statement = select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto_id)
        return list(self.session.exec(statement).all())

    def get_categoria_links(self, producto_id: int) -> list[ProductoCategoria]:
        statement = select(ProductoCategoria).where(ProductoCategoria.producto_id == producto_id)
        return list(self.session.exec(statement).all())

    def get_ingrediente_link(self, producto_id: int, ingrediente_id: int) -> Optional[ProductoIngrediente]:
        return self.session.get(ProductoIngrediente, (producto_id, ingrediente_id))

    def add_ingrediente_link(self, producto_id: int, ingrediente_id: int, cantidad: float, unidad_medida_id: int) -> ProductoIngrediente:
        link = ProductoIngrediente(
            producto_id=producto_id,
            ingrediente_id=ingrediente_id,
            cantidad=cantidad,
            unidad_medida_id=unidad_medida_id,
        )
        self.session.add(link)
        return link

    def add_categoria_link(self, producto_id: int, categoria_id: int) -> ProductoCategoria:
        link = ProductoCategoria(producto_id=producto_id, categoria_id=categoria_id)
        self.session.add(link)
        return link

    def delete_ingrediente_link(self, link: ProductoIngrediente):
        self.session.delete(link)

    def delete_categoria_link(self, link: ProductoCategoria):
        self.session.delete(link)

    def refresh(self, entity):
        self.session.refresh(entity)

    def flush(self):
        self.session.flush()
