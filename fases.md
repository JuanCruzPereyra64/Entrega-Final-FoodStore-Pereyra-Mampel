# Plan de Entrega — Food Store v6.0

Orden cronológico recomendado. Cada fase depende de la anterior.

---

## FASE 1 — Bugs que rompen funcionalidad

- [x] **BUG-01: `GestorPedidosPage` usa `EN_CAMINO` (no existe en v7)**
  `frontend/admin/src/pages/GestorPedidosPage.tsx` — Corregido: reemplazado EN_CAMINO por EN_PREP/ENTREGADO. Botón "Despachar" → "Entregado", badge/labels actualizados.
- [x] **BUG-02: Admin login ignora JWT Bearer**
  Corregido: `authApi.login()` ahora recibe `TokenResponse` con `access_token`. `useAuthStore` persiste el token. `LoginPage` llama `authApi.me()` post-login para obtener roles. Token disponible para WS.
  *Archivos*: `frontend/admin/src/services/api.ts`, `frontend/admin/src/pages/LoginPage.tsx`, `frontend/admin/src/store/useAuthStore.ts`
- [x] **BUG-03: Tipos TypeScript divergentes entre store y admin**
  Corregido: `int` → `number` en admin. `ProductoDetallePage.tsx` renderiza `unidad_medida?.nombre` en vez del objeto. Divergencia `_snap` vs sin sufijo es intencional (admin usa campos sin snap para backoffice).

---

## FASE 2 — Backend: Rate Limiting

- [x] **RL-01: Rate limiting en login/register**
  Implementado con `slowapi` + `Limiter(key_func=get_remote_address)`. Límite: 5 requests cada 15 minutos en `POST /registro` y `POST /login`. Respuesta `429 Too Many Requests` con header `Retry-After`.
  *Archivos*: `backend/core/limiter.py`, `backend/main.py`, `backend/routers/usuarios.py`, `backend/requirements.txt`

---

## FASE 3 — Frontend Admin: WebSocket en tiempo real

- [x] **AD-WS-01: Hook `useAdminOrdersFeed`**
  Creado hook con conexión WS, reconexión cada 3s, ping cada 25s, invalida `['pedidos']` al recibir eventos. Retorna `isConnected` para UI.
  *Archivos*: `frontend/admin/src/hooks/useAdminOrdersFeed.ts`
- [x] **AD-WS-02: Badge de conexión WS en sidebar**
  Indicador "🟢 Tiempo real activo" / "🔴 Sin conexión" en sidebar footer con bola de color.
  *Archivos*: `frontend/admin/src/components/layout/MainLayout.tsx`
- [x] **AD-WS-03: Sonner + toasts en admin**
  `sonner` instalado, `<Toaster richColors />` en MainLayout. Toasts en `updateMutation` (success/error) de GestorPedidosPage.
  *Archivos*: `frontend/admin/src/pages/GestorPedidosPage.tsx`, `frontend/admin/src/components/layout/MainLayout.tsx`, `frontend/admin/package.json`

---

## FASE 4 — Frontend Admin: Dashboard con gráficos (recharts)

- [x] **AD-CH-01: Instalar recharts**
  `npm install recharts` en `frontend/admin/`
- [x] **AD-CH-02: Dashboard con gráficos en HomePage**
  4 KPI cards desde `/estadisticas/resumen`, LineChart ventas 7 días, BarChart top 5 productos, PieChart pedidos por estado, BarChart ingresos por forma de pago. Stats grid + hero sección reemplazadas.
  *Archivos*: `frontend/admin/src/pages/HomePage.tsx`, `frontend/admin/src/services/api.ts`, `frontend/admin/src/types/index.ts`

---

## FASE 5 — Frontend Store: Stores faltantes (Zustand)

- [x] **ST-ST-01: wsStore**
  Creado con `{ isConnected, lastEvent, reconnectAttempts, setConnected, setLastEvent, incrementReconnect, resetReconnect }`. Integrado con `useOrderStatusWS.ts`. Sin persistencia.
  *Archivos*: `frontend/store/src/store/useWsStore.ts`, `frontend/store/src/hooks/useOrderStatusWS.ts`
- [x] **ST-ST-02: paymentStore**
  Creado con `{ status: 'idle' | 'processing' | 'success' | 'error', mpPaymentId, errorMessage, setProcessing, setSuccess, setError, reset }`.
  *Archivos*: `frontend/store/src/store/usePaymentStore.ts`
- [x] **ST-ST-03: uiStore**
  Creado con `{ sidebarOpen, toggleSidebar, setSidebarOpen }`.
  *Archivos*: `frontend/store/src/store/useUiStore.ts`

---

## FASE 6 — UX/UI Polish

- [x] **UX-01: Skeleton loaders**
  Creado componente `Skeleton` en common de ambos frontends. Reemplazados spinners en HomePage (store), PedidosPage (store), GestorPedidosPage (admin), VentasPage (admin), ProductosPage (admin).
  *Archivos*: `frontend/store/src/components/common/Skeleton.tsx`, `frontend/admin/src/components/common/Skeleton.tsx`, 5 pages actualizadas.
- [x] **UX-02: Transformaciones Cloudinary en imágenes**
  Creado `cloudinaryUrl()` util que agrega `f_auto,q_auto,c_fill,w_400` solo a URLs de Cloudinary. Aplicado en HomePage (store) y PedidosPage (store). Admin ProductosPage preview sin transformar (puede ser URL local).
  *Archivos*: `frontend/store/src/utils/cloudinary.ts`, `frontend/store/src/pages/HomePage.tsx`, `frontend/store/src/pages/PedidosPage.tsx`
- [x] **UX-03: Estados vacíos consistentes**
  Revisados todos los estados vacíos — ya usan icono + texto de forma consistente en ambos frontends. Sin cambios necesarios.

---

## FASE 7 — Tests automatizados (pytest + TestClient)

- [x] **TS-01: conftest.py**
  Fixtures: `engine` (SQLite in-memory + StaticPool), `setup_db` (autouse: create/seed/drop), `client`, `admin_headers`, `client_headers`. Rate limiter deshabilitado en tests via `app.state.limiter.enabled = False`.
  *Archivos*: `backend/tests/conftest.py`
- [x] **TS-02: test_auth.py**
  register OK, email duplicado (400), login OK, login inválido (401), logout con revocación (204), me autenticado, me no autenticado (401). 7 tests.
  *Archivos*: `backend/tests/test_auth.py`
- [x] **TS-03: test_pedidos.py**
  listar vacío, crear OK (201), stock insuficiente (400), cliente lista sus pedidos, cancelar propio, transicionar CONFIRMADO→ENTREGADO, terminal rechaza (400), cliente no puede transicionar (403). 8 tests.
  *Archivos*: `backend/tests/test_pedidos.py`
- [x] **TS-04: test_estadisticas.py**
  resumen, ventas período, productos top, pedidos por estado, ingresos, forbidden para no-admin. 6 tests.
  *Archivos*: `backend/tests/test_estadisticas.py`

---

## FASE 8 — Infraestructura y Checklist de Entrega

- [x] **IN-01: `.env.example` en frontends**
  Creados `frontend/store/.env.example` y `frontend/admin/.env.example` con `VITE_API_URL=http://localhost:8000`.
- [x] **IN-02: README.md actualizado**
  README.md ya existía con setup completo desde clonar repo. Verificado que incluye: .env, seed, backend, frontends, usuarios demo.
- [x] **IN-03: Verificar checklist CE-01 a CE-16**
  - CE-01: ✅ Repositorio GitHub público
  - CE-02: ✅ README setup completo verificado
  - CE-03: ✅ .env.example creado en backend y frontends
  - CE-05: ✅ `python backend/seed.py` funciona
  - CE-09: ⚠️ MP sandbox necesita credenciales reales para test end-to-end
  - CE-11: ✅ 5 Zustand stores: useAuthStore, useWsStore, usePaymentStore, useUiStore + cartStore
  - CE-12: ✅ WS: broadcast al cambiar estado desde admin → UI cliente
  - CE-13: ✅ Cloudinary: subir imagen desde admin → catálogo store
  - CE-15: ❓ Link a video demo en README — verificar que el link de YouTube sea correcto

---

## Resumen de impacto por rúbrica

| Item de rúbrica | Pts | Fase que lo cubre |
|---|---|---|
| Rate limiting | 10 (incluido en Estructura) | Fase 2 |
| Tests con TestClient | 20 | Fase 7 |
| Zustand (5 stores) | 10 | Fase 5 |
| Frontend WebSocket admin | 20 | Fase 3 |
| Frontend Estadísticas (recharts) | 10 | Fase 4 |
| UI/UX (skeletons, toasts, badge WS) | 10 | Fase 6 |
| Infraestructura (README, env) | — (penalización -30%) | Fase 8 |
