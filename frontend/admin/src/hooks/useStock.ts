import { useQuery } from '@tanstack/react-query'
import { stockApi } from '../services/api'

export function useMovimientosStock(ingredienteId?: number) {
  return useQuery({
    queryKey: ['movimientos_stock', ingredienteId],
    queryFn: () => stockApi.getMovimientos(ingredienteId),
  })
}
