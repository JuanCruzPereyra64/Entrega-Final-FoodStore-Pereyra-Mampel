import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'sonner'
import { MainLayout } from './components/layout/MainLayout'
import { HomePage } from './pages/HomePage'
import { CartPage } from './pages/CartPage'
import { PedidosPage } from './pages/PedidosPage'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import { PerfilPage } from './pages/PerfilPage'

function App() {
  return (
    <>
      <Toaster richColors position="top-right" duration={2000} />
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/*" element={
            <MainLayout>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/carrito" element={<CartPage />} />
                <Route path="/mis-pedidos" element={<PedidosPage />} />
                <Route path="/mi-perfil" element={<PerfilPage />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </MainLayout>
          } />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
