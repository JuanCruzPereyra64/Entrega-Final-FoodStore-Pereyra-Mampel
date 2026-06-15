import { create } from 'zustand'

type PaymentStatus = 'idle' | 'processing' | 'success' | 'error'

interface PaymentState {
  status: PaymentStatus
  mpPaymentId: number | null
  errorMessage: string | null
  setProcessing: () => void
  setSuccess: (mpPaymentId: number) => void
  setError: (message: string) => void
  reset: () => void
}

export const usePaymentStore = create<PaymentState>((set) => ({
  status: 'idle',
  mpPaymentId: null,
  errorMessage: null,
  setProcessing: () => set({ status: 'processing', errorMessage: null }),
  setSuccess: (mpPaymentId) => set({ status: 'success', mpPaymentId, errorMessage: null }),
  setError: (message) => set({ status: 'error', errorMessage: message }),
  reset: () => set({ status: 'idle', mpPaymentId: null, errorMessage: null }),
}))
