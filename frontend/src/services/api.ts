import axios from 'axios'
import { CardapioResponse, Produto } from '@/types/cardapio.types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const cardapioApi = {
  getCardapioCompleto: async (): Promise<CardapioResponse> => {
    const response = await api.get<CardapioResponse>('/cardapio/')
    return response.data
  },

  getProdutosPorCategoria: async (
    categoriaId: number,
    incluirIndisponiveis = false
  ): Promise<Produto[]> => {
    const response = await api.get<Produto[]>(
      `/cardapio/categorias/${categoriaId}/produtos`,
      { params: { incluir_indisponiveis: incluirIndisponiveis } }
    )
    return response.data
  },

  buscarProdutos: async (termo: string): Promise<Produto[]> => {
    const response = await api.get<Produto[]>('/cardapio/buscar', {
      params: { termo },
    })
    return response.data
  },
}

export default api
