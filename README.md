# E-Commerce Food Store — Programación 4 (Segundo Parcial)

Video: https://www.youtube.com/watch?v=hzjdq_WjNwA

Aplicación web Full-Stack para la gestión y venta de productos alimenticios (E-Commerce), separada en dos módulos principales: una tienda para clientes y un panel de administración para empleados/dueños.

**Tecnologías Principales:**
- **Backend:** Python, FastAPI, SQLModel (SQLAlchemy + Pydantic), SQLite
- **Frontend (Store & Admin):** React, TypeScript, Vite, Tailwind CSS 4, Zustand, TanStack Query (React Query), React Router DOM

## Arquitectura del Proyecto

El proyecto está dividido en tres partes fundamentales:

- `backend/`: API RESTful encargada de la lógica de negocio, autenticación mediante JWT (HttpOnly Cookies), y persistencia de datos relacional con SQLite.
- `frontend/store/`: Interfaz de usuario pública (E-Commerce) donde los clientes pueden navegar por el catálogo de productos y agregar items al carrito.
- `frontend/admin/`: Panel de control privado protegido por roles (ADMIN, STOCK) para la gestión del catálogo de productos, categorías, ingredientes y el seguimiento/cambio de estados de los pedidos.

## Setup y Ejecución (Desarrollo Local)

### Requisitos Previos
- Python 3.10+
- Node.js 18+

### 1. Iniciar el Backend

El backend utiliza una base de datos SQLite embebida (`parcial_db.db`), por lo que no es necesario instalar motores de bases de datos adicionales ni Docker.

```bash
# Navegar a la carpeta raíz del proyecto
# Instalar dependencias
pip install -r backend/requirements.txt

# (Opcional) Ejecutar el Seed para cargar roles, estados de pedido y usuarios de prueba
python -m backend.seed

# Levantar el servidor de FastAPI
uvicorn backend.main:app --reload
```
- **API disponible en:** http://localhost:8000
- **Documentación Swagger:** http://localhost:8000/docs

*Credenciales por defecto creadas por el Seed:*
- **Admin:** `admin@admin.com` | Password: `admin`
- **Cliente:** `test@test.com` | Password: `123456`

### 2. Iniciar Frontend - E-Commerce (Store)

```bash
cd frontend/store
npm install
npm run dev
```
- **Store disponible en:** http://localhost:5173

### 3. Iniciar Frontend - Panel de Administración (Admin)

En una terminal separada:
```bash
cd frontend/admin
npm install
npm run dev
```
- **Admin disponible en:** http://localhost:5174

## Características Técnicas Destacadas

- **Autenticación Segura:** JWT transmitidos por cookies `HttpOnly` para prevenir ataques XSS.
- **Autorización por Roles:** Rutas y endpoints protegidos dependiendo de si el usuario es `CLIENT`, `ADMIN` o `STOCK`.
- **Soft Deletes:** Implementado en el modelo de base de datos para no eliminar registros permanentemente.
- **Server State Management:** Uso extensivo de TanStack Query para fetching, mutaciones, caché e invalidación de datos instantánea sin recargar la página.
- **Persistencia Local:** Estado del carrito mantenido en `localStorage` mediante Zustand persist.

## Video de Demostración
[Link al video de la presentación]
