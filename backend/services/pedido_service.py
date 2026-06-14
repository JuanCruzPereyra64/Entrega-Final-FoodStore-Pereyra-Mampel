from decimal import Decimal
from fastapi import HTTPException, status
from backend.models.pedido import Pedido
from backend.models.detalle_pedido import DetallePedido
from backend.models.historial_estado_pedido import HistorialEstadoPedido
from backend.schemas.pedido import PedidoCreate
from backend.uow.unit_of_work import UnitOfWork
from sqlmodel import select
from backend.models.producto import ProductoIngrediente
from backend.models.ingrediente import Ingrediente
from backend.services import movimiento_stock_service

def crear_pedido(uow: UnitOfWork, usuario_id: int, data: PedidoCreate) -> Pedido:
    subtotal = Decimal('0.00')
    detalles_models = []
    
    # 1. Procesar detalles y calcular totales (Snapshot pattern)
    for det_data in data.detalles:
        producto = uow.productos.get_by_id(det_data.producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {det_data.producto_id} no encontrado")
            
        precio_snap = Decimal(str(producto.precio_base))
        nombre_snap = producto.nombre
        subtotal_detalle = precio_snap * det_data.cantidad
        subtotal += subtotal_detalle
        
        detalle = DetallePedido(
            producto_id=producto.id,
            cantidad=det_data.cantidad,
            nombre_producto_snap=nombre_snap,
            precio_unitario_snap=precio_snap,
            subtotal_snap=subtotal_detalle,
            personalizacion=det_data.personalizacion
        )
        detalle.producto = producto
        detalles_models.append(detalle)
        
        # Validar stock disponible (sin descontar aún — se descuenta al confirmar)
        links_ing = uow.session.exec(select(ProductoIngrediente).where(ProductoIngrediente.producto_id == producto.id)).all()
        for link in links_ing:
            ing = uow.session.get(Ingrediente, link.ingrediente_id)
            if ing:
                cantidad_a_consumir = link.cantidad_requerida * det_data.cantidad
                if ing.stock_actual < cantidad_a_consumir:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Stock insuficiente de '{ing.nombre}' para preparar '{producto.nombre}'. Requerido: {cantidad_a_consumir}, Disponible: {ing.stock_actual}"
                    )
        
    costo_envio = Decimal('500.00')  # Hardcoded. Podría provenir de config o logística.
    descuento = Decimal('0.00')
    total = subtotal + costo_envio - descuento
    
    # 2. Crear Pedido
    pedido = Pedido(
        usuario_id=usuario_id,
        direccion_id=data.direccion_id,
        estado_codigo='PENDIENTE',
        forma_pago_codigo=data.forma_pago_codigo,
        subtotal=subtotal,
        descuento=descuento,
        costo_envio=costo_envio,
        total=total,
        notas=data.notas,
        detalles=detalles_models
    )
    
    uow.pedidos.add(pedido)
    uow.session.flush()  # Para que pedido tenga ID
    
    # 3. Crear Primer Historial
    historial = HistorialEstadoPedido(
        pedido_id=pedido.id,
        estado_desde=None,
        estado_hacia='PENDIENTE',
        usuario_id=usuario_id,
        motivo='Creación inicial del pedido'
    )
    uow.session.add(historial)
    uow.session.flush()
    
    uow.session.refresh(pedido)
    return pedido


def transicionar_estado(uow: UnitOfWork, pedido_id: int, nuevo_estado_codigo: str, usuario_id: int, motivo: str = None) -> Pedido:
    pedido = uow.pedidos.get_by_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
    # Validar REGLA DE NEGOCIO ESTRICTA (Terminal)
    estado_actual = uow.estados_pedido.get_by_codigo(pedido.estado_codigo)
    if not estado_actual:
        raise HTTPException(status_code=500, detail="Estado actual del pedido es inválido")
        
    if estado_actual.es_terminal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"El pedido no puede cambiar de estado porque el estado actual ({estado_actual.codigo}) es terminal."
        )
        
    nuevo_estado = uow.estados_pedido.get_by_codigo(nuevo_estado_codigo)
    if not nuevo_estado:
        raise HTTPException(status_code=400, detail="El nuevo estado proporcionado no existe.")
        
    estado_anterior = pedido.estado_codigo
    pedido.estado_codigo = nuevo_estado_codigo

    # Descuento de stock al confirmar
    if nuevo_estado_codigo == 'CONFIRMADO':
        for detalle in pedido.detalles:
            links_ing = uow.session.exec(
                select(ProductoIngrediente).where(ProductoIngrediente.producto_id == detalle.producto_id)
            ).all()
            for link in links_ing:
                ing = uow.session.get(Ingrediente, link.ingrediente_id)
                if ing:
                    cantidad_a_consumir = link.cantidad_requerida * detalle.cantidad
                    if ing.stock_actual < cantidad_a_consumir:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Stock insuficiente de '{ing.nombre}'. Requerido: {cantidad_a_consumir}, Disponible: {ing.stock_actual}"
                        )
                    ing.stock_actual -= cantidad_a_consumir
                    uow.session.add(ing)
                    movimiento_stock_service.registrar_movimiento(
                        uow,
                        ingrediente_id=ing.id,
                        cantidad=-cantidad_a_consumir,
                        motivo=f"Venta confirmada (Pedido #{pedido.id})",
                        usuario_id=usuario_id
                    )

    # Devolver stock si se cancela un pedido ya confirmado
    if nuevo_estado_codigo == 'CANCELADO' and estado_anterior == 'CONFIRMADO':
        for detalle in pedido.detalles:
            links_ing = uow.session.exec(
                select(ProductoIngrediente).where(ProductoIngrediente.producto_id == detalle.producto_id)
            ).all()
            for link in links_ing:
                ing = uow.session.get(Ingrediente, link.ingrediente_id)
                if ing:
                    cantidad_a_devolver = link.cantidad_requerida * detalle.cantidad
                    ing.stock_actual += cantidad_a_devolver
                    uow.session.add(ing)
                    movimiento_stock_service.registrar_movimiento(
                        uow,
                        ingrediente_id=ing.id,
                        cantidad=cantidad_a_devolver,
                        motivo=f"Cancelación de pedido confirmado (Pedido #{pedido.id})",
                        usuario_id=usuario_id
                    )

    # Historial Append-only
    historial = HistorialEstadoPedido(
        pedido_id=pedido.id,
        estado_desde=estado_anterior,
        estado_hacia=nuevo_estado_codigo,
        usuario_id=usuario_id,
        motivo=motivo
    )
    
    uow.session.add(historial)
    uow.session.flush()
    uow.session.refresh(pedido)
    
    return pedido

def get_all(uow: UnitOfWork):
    return uow.pedidos.get_all()

def get_by_usuario(uow: UnitOfWork, usuario_id: int):
    return uow.pedidos.get_by_usuario_id(usuario_id)

def cancelar_pedido_cliente(uow: UnitOfWork, pedido_id: int, usuario_id: int) -> Pedido:
    pedido = uow.pedidos.get_by_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
    if pedido.usuario_id != usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para cancelar este pedido")
        
    if pedido.estado_codigo not in ['PENDIENTE', 'CONFIRMADO']:
        raise HTTPException(
            status_code=400, 
            detail=f"Solo podés cancelar pedidos en estado PENDIENTE o CONFIRMADO. Estado actual: {pedido.estado_codigo}"
        )
        
    return transicionar_estado(uow, pedido_id, 'CANCELADO', usuario_id, motivo='Cancelado por el cliente')
