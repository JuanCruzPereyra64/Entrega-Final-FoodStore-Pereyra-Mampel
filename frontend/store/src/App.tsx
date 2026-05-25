import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { MainLayout } from './components/layout/MainLayout'
import { HomePage } from './pages/HomePage'
import { CartPage } from './pages/CartPage'
import { PedidosPage } from './pages/PedidosPage'
import { LoginPage } from './pages/LoginPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/*" element={
          <MainLayout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/carrito" element={<CartPage />} />
              <Route path="/mis-pedidos" element={<PedidosPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </MainLayout>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default App
