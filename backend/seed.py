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
from backend.models.producto import Producto, ProductoCategoria, ProductoIngrediente
from backend.models.unidad_medida import UnidadMedida

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def run_seed():
    print("Iniciando Seed de Base de Datos Súper Completo...")
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
        formas_pago = ["EFECTIVO", "MERCADOPAGO", "TARJETA_CREDITO", "TARJETA_DEBITO"]
        for codigo in formas_pago:
            if not uow.session.exec(select(FormaPago).where(FormaPago.codigo == codigo)).first():
                uow.session.add(FormaPago(codigo=codigo, descripcion=f"Pago mediante {codigo}"))
                
        uow.session.flush()
        
        print("Creando Usuarios...")
        usuarios_seed = [
            ("test@test.com", "Test", "User", "123456", "CLIENT"),
            ("admin@admin.com", "Admin", "Gómez", "admin", "ADMIN"),
            ("cajero@food.com", "Carlos", "Cajero", "123456", "PEDIDOS"),
            ("stock@food.com", "Sofía", "Stock", "123456", "STOCK"),
        ]
        
        for email, nombre, apellido, pwd, rol_codigo in usuarios_seed:
            user = uow.usuarios.get_by_email(email)
            if not user:
                hash_pwd = pwd_context.hash(pwd)
                user = Usuario(nombre=nombre, apellido=apellido, email=email, password_hash=hash_pwd)
                uow.usuarios.add(user)
                uow.session.flush()
                rol = uow.session.exec(select(Rol).where(Rol.nombre == rol_codigo)).first()
                if rol:
                    uow.session.add(UsuarioRol(usuario_id=user.id, rol_id=rol.id))
                
        print("Creando Categorías...")
        categorias_data = [
            ("Hamburguesas", "Nuestras clásicas y especiales"),
            ("Pizzas", "A la piedra y masa madre"),
            ("Bebidas", "Refrescos y cervezas"),
            ("Postres", "Para terminar con algo dulce"),
            ("Papas Fritas", "El acompañamiento ideal")
        ]
        categorias_obj = {}
        for c_nombre, c_desc in categorias_data:
            cat = uow.session.exec(select(Categoria).where(Categoria.nombre == c_nombre)).first()
            if not cat:
                cat = Categoria(nombre=c_nombre, descripcion=c_desc)
                uow.session.add(cat)
                uow.session.flush()
            categorias_obj[c_nombre] = cat

        print("Creando Unidades de Medida...")
        unidades_data = ["g", "ml", "u", "kg"]
        unidades_obj = {}
        for u_nombre in unidades_data:
            um = uow.session.exec(select(UnidadMedida).where(UnidadMedida.nombre == u_nombre)).first()
            if not um:
                um = UnidadMedida(nombre=u_nombre)
                uow.session.add(um)
                uow.session.flush()
            unidades_obj[u_nombre] = um

        print("Creando Ingredientes...")
        ingredientes_data = [
            ("Pan de Papa", False, "u"), ("Medallón 120g", False, "g"), ("Queso Cheddar", False, "g"),
            ("Panceta Crocante", False, "g"), ("Salsa BBQ", False, "ml"), ("Cebolla Caramelizada", False, "g"),
            ("Masa Madre", False, "g"), ("Salsa de Tomate", False, "ml"), ("Muzzarella", False, "g"),
            ("Pepperoni", False, "g"), ("Papas Bastón", False, "g"), ("Helado de Vainilla", False, "g"),
            ("Brownie", True, "u"), ("Tomate Fresco", False, "u"), ("Lechuga", False, "g")
        ]
        ingredientes_obj = {}
        for i_nombre, alergeno, unidad in ingredientes_data:
            ing = uow.session.exec(select(Ingrediente).where(Ingrediente.nombre == i_nombre)).first()
            if not ing:
                ing = Ingrediente(nombre=i_nombre, es_alergeno=alergeno, unidad_medida_id=unidades_obj[unidad].id)
                uow.session.add(ing)
                uow.session.flush()
            ingredientes_obj[i_nombre] = ing
            
        print("Creando Productos...")
        productos_data = [
            {
                "nombre": "Doble Queso Bacon",
                "descripcion": "Doble medallón, cuádruple cheddar, panceta crocante y pan de papa.",
                "precio": 8500,
                "stock": 50,
                "categoria": "Hamburguesas",
                "ingredientes": ["Pan de Papa", "Medallón 120g", "Queso Cheddar", "Panceta Crocante"]
            },
            {
                "nombre": "Classic Burger",
                "descripcion": "Medallón simple con lechuga, tomate y queso cheddar.",
                "precio": 6500,
                "stock": 100,
                "categoria": "Hamburguesas",
                "ingredientes": ["Pan de Papa", "Medallón 120g", "Queso Cheddar", "Lechuga", "Tomate Fresco"]
            },
            {
                "nombre": "Pizza Pepperoni",
                "descripcion": "Masa madre, salsa, extra muzzarella y pepperoni premium.",
                "precio": 12000,
                "stock": 30,
                "categoria": "Pizzas",
                "ingredientes": ["Masa Madre", "Salsa de Tomate", "Muzzarella", "Pepperoni"]
            },
            {
                "nombre": "Pizza Margarita",
                "descripcion": "La clásica de masa madre con salsa y muzzarella.",
                "precio": 10000,
                "stock": 40,
                "categoria": "Pizzas",
                "ingredientes": ["Masa Madre", "Salsa de Tomate", "Muzzarella"]
            },
            {
                "nombre": "Papas con Cheddar y Panceta",
                "descripcion": "Porción abundante bañada en cheddar fundido y lluvia de panceta.",
                "precio": 4500,
                "stock": 200,
                "categoria": "Papas Fritas",
                "ingredientes": ["Papas Bastón", "Queso Cheddar", "Panceta Crocante"]
            },
            {
                "nombre": "Volcán de Chocolate",
                "descripcion": "Volcán tibio de chocolate (brownie) con bocha de helado de vainilla.",
                "precio": 5500,
                "stock": 15,
                "categoria": "Postres",
                "ingredientes": ["Brownie", "Helado de Vainilla"]
            },
            {
                "nombre": "Coca Cola 500ml",
                "descripcion": "Gaseosa línea Coca Cola bien fría.",
                "precio": 1500,
                "stock": 300,
                "categoria": "Bebidas",
                "ingredientes": []
            }
        ]
        
        for p_data in productos_data:
            prod = uow.session.exec(select(Producto).where(Producto.nombre == p_data["nombre"])).first()
            if not prod:
                prod = Producto(
                    nombre=p_data["nombre"],
                    descripcion=p_data["descripcion"],
                    precio_base=p_data["precio"],
                    stock_cantidad=p_data["stock"],
                    disponible=True,
                    tiempo_prep_min=15
                )
                uow.session.add(prod)
                uow.session.flush()
                
                # Asignar categoría
                cat = categorias_obj[p_data["categoria"]]
                uow.session.add(ProductoCategoria(producto_id=prod.id, categoria_id=cat.id, es_principal=True))
                
                # Asignar ingredientes
                for ing_name in p_data["ingredientes"]:
                    ing = ingredientes_obj[ing_name]
                    uow.session.add(ProductoIngrediente(producto_id=prod.id, ingrediente_id=ing.id, es_removible=True, es_opcional=False))
                    
        print("Seed Súper Completo finalizado con éxito. Base de datos lista.")

if __name__ == "__main__":
    run_seed()
