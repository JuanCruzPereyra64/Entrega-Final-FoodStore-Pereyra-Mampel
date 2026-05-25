from decimal import Decimal
from fastapi import HTTPException, status
from backend.models.pedido import Pedido
from backend.models.detalle_pedido import DetallePedido
from backend.models.historial_estado_pedido import HistorialEstadoPedido
from backend.schemas.pedido import PedidoCreate
from backend.uow.unit_of_work import UnitOfWork

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
        detalles_models.append(detalle)
        
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
