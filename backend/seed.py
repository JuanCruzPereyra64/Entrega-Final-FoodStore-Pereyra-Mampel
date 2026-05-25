import sys
import os
from sqlmodel import select
from passlib.context import CryptContext

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import create_db_and_tables
from backend.uow.unit_of_work import UnitOfWork
from backend.models.rol import Rol
from backend.models.estado_pedido import EstadoPedido
from backend.models.forma_pago import FormaPago
from backend.models.usuario import Usuario
from backend.models.usuario_rol import UsuarioRol
from backend.models.categoria import Categoria
from backend.models.ingrediente import Ingrediente

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def run_seed():
    print("Iniciando Seed de Base de Datos...")
    create_db_and_tables()
    
    uow = UnitOfWork()
    with uow:
        print("Poblando Roles...")
        roles = ["ADMIN", "STOCK", "PEDIDOS", "CLIENT"]
        for r_name in roles:
            if not uow.session.exec(select(Rol).where(Rol.nombre == r_name)).first():
                uow.session.add(Rol(nombre=r_name, descripcion=f"Rol {r_name}"))
        
        print("Poblando Estados de Pedido...")
        estados = [
            ("PENDIENTE", "Pedido recibido", 1, False),
            ("CONFIRMADO", "Pedido confirmado", 2, False),
            ("EN_PREP", "En preparación", 3, False),
            ("EN_CAMINO", "En camino", 4, False),
            ("ENTREGADO", "Entregado", 5, True),
            ("CANCELADO", "Cancelado", 6, True)
        ]
        for codigo, desc, orden, terminal in estados:
            if not uow.estados_pedido.get_by_codigo(codigo):
                uow.session.add(EstadoPedido(
                    codigo=codigo, descripcion=desc, orden=orden, es_terminal=terminal
                ))
                
        print("Poblando Formas de Pago...")
        formas_pago = ["EFECTIVO", "MERCADOPAGO"]
        for codigo in formas_pago:
            if not uow.session.exec(select(FormaPago).where(FormaPago.codigo == codigo)).first():
                uow.session.add(FormaPago(codigo=codigo, descripcion=f"Pago mediante {codigo}"))
                
        uow.session.flush()
        
        print("Creando Usuario Test...")
        email = "test@test.com"
        if not uow.usuarios.get_by_email(email):
            hash_pwd = pwd_context.hash("123456")
            user = Usuario(
                nombre="Test", apellido="User", email=email, password_hash=hash_pwd
            )
            uow.usuarios.add(user)
            uow.session.flush()
            
            rol_cliente = uow.session.exec(select(Rol).where(Rol.nombre == "CLIENT")).first()
            if rol_cliente:
                uow.session.add(UsuarioRol(usuario_id=user.id, rol_id=rol_cliente.id))
                
        print("Creando Usuario Admin...")
        admin_email = "admin@admin.com"
        if not uow.usuarios.get_by_email(admin_email):
            hash_pwd = pwd_context.hash("admin")
            admin_user = Usuario(
                nombre="Admin", apellido="Admin", email=admin_email, password_hash=hash_pwd
            )
            uow.usuarios.add(admin_user)
            uow.session.flush()
            
            rol_admin = uow.session.exec(select(Rol).where(Rol.nombre == "ADMIN")).first()
            if rol_admin:
                uow.session.add(UsuarioRol(usuario_id=admin_user.id, rol_id=rol_admin.id))
                
        print("Creando Categoria e Ingredientes Básicos...")
        if not uow.session.exec(select(Categoria).where(Categoria.nombre == "Hamburguesas")).first():
            uow.session.add(Categoria(nombre="Hamburguesas", descripcion="Nuestras clásicas"))
            
        ingredientes = ["Pan de Papa", "Medallón 120g", "Queso Cheddar"]
        for ing_name in ingredientes:
            if not uow.session.exec(select(Ingrediente).where(Ingrediente.nombre == ing_name)).first():
                uow.session.add(Ingrediente(nombre=ing_name, es_alergeno=False))

    print("Seed finalizado con éxito. Base de datos lista.")

if __name__ == "__main__":
    run_seed()
