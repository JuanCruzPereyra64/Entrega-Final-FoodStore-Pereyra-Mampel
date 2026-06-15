import { useEffect, useRef, useState } from 'react'
import { toast } from 'sonner'
import { initMercadoPago } from '@mercadopago/sdk-react'
import { pagosApi, authApi } from '../../services/api'
import { Button } from '../common/Button'
import { ArrowLeft, CreditCard, Loader2 } from 'lucide-react'

interface PaymentStepProps {
  pedidoId: number
  total: number
  onSuccess: () => void
  onBack: () => void
}

export function PaymentStep({ pedidoId, total, onSuccess, onBack }: PaymentStepProps) {
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const brickRef = useRef(false)

  useEffect(() => {
    async function init() {
      try {
        const [keyRes, user] = await Promise.all([
          pagosApi.getPublicKey(),
          authApi.me(),
        ])

        if (!keyRes.public_key) {
          setError('MercadoPago no está configurado')
          setLoading(false)
          return
        }

        initMercadoPago(keyRes.public_key, { locale: 'es-AR' })
        setLoading(false)

        await renderBrick(keyRes.public_key, user.email)
      } catch {
        setError('Error al conectar con MercadoPago')
        setLoading(false)
      }
    }

    async function renderBrick(publicKey: string, email: string) {
      await new Promise(r => setTimeout(r, 500))

      if (brickRef.current) return
      brickRef.current = true

      const container = document.getElementById('cardPaymentBrick_container')
      if (!container) return

      const mp = new (window as any).MercadoPago(publicKey, { locale: 'es-AR' })

      mp.bricks().create('cardPayment', 'cardPaymentBrick_container', {
        initialization: { amount: total, payer: { email } },
        callbacks: {
          onSubmit: async (param: any) => {
            try {
              const res = await pagosApi.crear({
                pedido_id: pedidoId,
                transaction_amount: total as any,
                card_token_id: param.token,
                email,
                payment_method_id: param.payment_method_id,
                installments: param.installments,
              })
              if (res.mp_status === 'approved') {
                toast.success('Pago aprobado exitosamente')
              } else if (res.mp_status === 'pending') {
                toast.success('Pago procesado, estamos esperando la confirmación')
              } else {
                toast.error(`Pago rechazado: ${res.mp_status_detail || res.mp_status}`)
                return
              }
              onSuccess()
            } catch (err: any) {
              toast.error(err.message || 'Error al procesar el pago')
            }
          },
          onError: () => {
            toast.error('Error en el formulario de pago')
          },
        },
      })
    }

    init()
  }, [pedidoId, total, onSuccess])

  if (loading) {
    return (
      <div className="flex justify-center py-10">
        <Loader2 size={32} className="animate-spin text-primary" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-10 space-y-4">
        <CreditCard size={48} className="mx-auto text-slate-300" />
        <p className="text-slate-500">{error}</p>
        <Button variant="secondary" onClick={onBack}>
          <ArrowLeft size={16} /> Volver
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <button onClick={onBack} className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-colors">
          <ArrowLeft size={20} />
        </button>
        <div>
          <h3 className="font-semibold">Pagar con MercadoPago</h3>
          <p className="text-sm text-slate-500">Total: ${total}</p>
        </div>
      </div>

      <div id="cardPaymentBrick_container" />
    </div>
  )
}
