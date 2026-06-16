# Guion Video — Food Store TPI Parcial 2

---

## [0:00 – 0:45] Introducción

**Pantalla:** cámara o diapositiva con nombres del equipo

> "Buenas, somos [nombres]. En este video vamos a presentar Food Store, nuestro TPI de Programación 4. El sistema es una aplicación full-stack de gestión de pedidos de comida, con React + TypeScript en el frontend, FastAPI + PostgreSQL en el backend, y WebSocket para tiempo real."

> "[Nombre 1] se encargó de [rol]. [Nombre 2] se encargó de [rol]."

---

## [0:45 – 1:30] Backend — Logs, Timing y Rate Limit

**Pantalla:** terminal con el servidor corriendo (`uvicorn backend.main:app`)

> "Arrancamos el backend. Cada request que llega se loggea con el método HTTP, el endpoint, el código de respuesta y el tiempo de procesamiento en milisegundos."

Hacer una request desde el browser para que aparezca en la terminal:

```
10:32:14 [INFO] GET /api/v1/productos → 200 (12.3 ms)
10:32:15 [INFO] POST /api/v1/auth/login → 200 (47.1 ms)
```

> "También tenemos rate limiting en login y registro — máximo 5 intentos por IP en 15 minutos. Si se supera, el servidor devuelve 429 Too Many Requests."

---

## [1:30 – 2:00] Backend — Exception Handler RFC 7807

**Pantalla:** Swagger (`/docs`) o terminal

> "El backend implementa el estándar RFC 7807 para manejo de errores. Todos los errores devuelven un JSON con `detail`, `code` y `field`."

Hacer una request inválida desde Swagger (por ejemplo POST /pedidos sin body) y mostrar la respuesta:

```json
{
  "detail": "field required",
  "code": "VALIDATION_ERROR",
  "field": "body.detalles"
}
```

---

## [2:00 – 4:00] Admin — Categorías y Subcategorías

**Pantalla:** panel de admin, sección Categorías

> "Entramos al panel de administración. Vamos a la sección de Categorías."

1. **Crear categoría raíz:** completar nombre → guardar → aparece en la lista
2. **Crear subcategoría:** mismo formulario, seleccionar la categoría padre → guardar
3. **Editar:** click en editar, cambiar el nombre → guardar

> "El sistema soporta jerarquía — una categoría puede tener subcategorías anidadas."

---

## [4:00 – 5:30] Admin — Ingredientes

**Pantalla:** panel de admin, sección Ingredientes

> "Ahora los ingredientes."

1. **Crear ingrediente:** nombre, unidad de medida, stock inicial, marcar si es alérgeno → guardar
2. **Editar:** cambiar el stock de un ingrediente existente → guardar

---

## [5:30 – 7:30] Admin — Productos

**Pantalla:** panel de admin, sección Productos

> "Ahora creamos un producto y lo asociamos con ingredientes."

1. **Crear producto:** nombre, precio, categoría, subir imagen (Cloudinary) → guardar
2. **Asociar ingrediente:** en el detalle del producto, agregar un ingrediente con su cantidad
3. **Editar:** modificar el precio → guardar

> "El precio se guarda como snapshot en cada pedido — si cambia después, los pedidos anteriores no se ven afectados."

---

## [7:30 – 8:30] Admin — Módulo de Estadísticas

**Pantalla:** panel de admin, sección Estadísticas / Dashboard

> "El panel tiene un módulo de estadísticas con métricas del negocio."

Mostrar los gráficos disponibles: ventas por período, productos más pedidos, pedidos por estado.

---

## [8:30 – 10:00] Cliente — Direcciones y Crear Pedido

**Pantalla:** store (localhost:5173), logueado como cliente

1. **Agregar dirección:** Mi Perfil → Agregar dirección → completar → guardar

> "El cliente puede tener múltiples direcciones y marcar una como principal."

2. **Agregar productos al carrito:** desde el catálogo, agregar 2 o 3 productos
3. **Ir al carrito:** mostrar resumen con subtotal, envío y total
4. **Checkout con Efectivo:** abrir modal → seleccionar dirección → seleccionar Efectivo → Confirmar pedido

> "El pedido se crea en estado PENDIENTE."

Terminal del backend visible:

```
POST /api/v1/pedidos → 201 (83.6 ms)
```

---

## [10:00 – 12:00] Cliente — Pasarela de Pago MercadoPago

**Pantalla:** store, carrito con productos

> "Ahora mostramos el flujo con MercadoPago."

1. Carrito → checkout → seleccionar **MercadoPago** → Confirmar pedido
2. El sistema redirige al sandbox de MercadoPago
3. Completar el pago con tarjeta de prueba
4. MercadoPago redirige de vuelta a `/mis-pedidos`

> "Una vez aprobado el pago, el webhook de MercadoPago notifica al backend y el pedido pasa automáticamente a CONFIRMADO."

Terminal visible:

```
POST /api/v1/pagos/webhook → 200 (31.2 ms)
```

---

## [12:00 – 14:30] Tiempo Real — Cambio de Estados vía WebSocket

**Pantalla:** dos ventanas lado a lado — store (cliente) y admin

> "Mostramos el cambio de estados en tiempo real."

Setup: store abierto en `/mis-pedidos` con el cliente logueado. Admin abierto en la sección de pedidos.

1. **Admin:** seleccionar el pedido → avanzar a **EN_PREP**
2. **Store:** el estado cambia en pantalla **sin recargar la página**

> "La notificación llega vía WebSocket al instante."

3. **Admin:** avanzar a **ENTREGADO**
4. **Store:** se actualiza nuevamente en tiempo real

---

## [14:30 – 15:30] Cliente — Cancelar Pedido

**Pantalla:** store, `/mis-pedidos`

> "El cliente también puede cancelar su propio pedido si está en PENDIENTE o CONFIRMADO."

1. Crear un pedido nuevo con Efectivo
2. Desde `/mis-pedidos`, hacer click en Cancelar → confirmar
3. El estado cambia a **CANCELADO** y se refleja de inmediato

---

## [15:30 – 16:00] Cierre

**Pantalla:** cámara o el código

> "Eso es todo. El sistema cubre el flujo completo: catálogo, carrito, pedidos, pagos con MercadoPago, WebSocket en tiempo real, gestión de stock con ingredientes, imágenes en Cloudinary y panel de administración. Gracias."

---

## Recomendaciones antes de grabar

- Tener el backend corriendo con la terminal visible en una mitad de la pantalla y el browser en la otra
- Preparar de antemano: una cuenta cliente, una cuenta admin, y al menos 2 productos con ingredientes cargados
- Usar las tarjetas de prueba oficiales del sandbox de MercadoPago
- Grabar en una sola toma si es posible — los cortes hacen perder tiempo y contexto
