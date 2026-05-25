import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { MainLayout } from './components/layout/MainLayout'
import { HomePage } from './pages/HomePage'
import { CategoriasPage } from './pages/CategoriasPage'
import { IngredientesPage } from './pages/IngredientesPage'
import { ProductosPage } from './pages/ProductosPage'
import { ProductoDetallePage } from './pages/ProductoDetallePage'
import { AuthGuard } from './components/layout/AuthGuard'
import { LoginPage } from './pages/LoginPage'
import { GestorPedidosPage } from './pages/GestorPedidosPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/*" element={
          <MainLayout>
            <Routes>
              <Route path="/unauthorized" element={<div className="p-10 text-center text-xl font-bold">No autorizado</div>} />
              <Route path="/" element={<AuthGuard allowedRoles={['ADMIN', 'STOCK', 'PEDIDOS']}><HomePage /></AuthGuard>} />
              <Route path="/categorias" element={<AuthGuard allowedRoles={['ADMIN', 'STOCK']}><CategoriasPage /></AuthGuard>} />
              <Route path="/ingredientes" element={<AuthGuard allowedRoles={['ADMIN', 'STOCK']}><IngredientesPage /></AuthGuard>} />
              <Route path="/productos" element={<AuthGuard allowedRoles={['ADMIN', 'STOCK']}><ProductosPage /></AuthGuard>} />
              <Route path="/productos/:id" element={<AuthGuard allowedRoles={['ADMIN', 'STOCK']}><ProductoDetallePage /></AuthGuard>} />
              <Route path="/pedidos" element={<AuthGuard allowedRoles={['ADMIN', 'PEDIDOS']}><GestorPedidosPage /></AuthGuard>} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </MainLayout>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default App
