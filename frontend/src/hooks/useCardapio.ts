import { useQuery } from '@tanstack/react-query';
import { cardapioApi } from '@/services/api';
import type { CardapioResponse, Produto } from '@/types/cardapio.types';

/**
 * Hook para buscar o cardápio completo (categorias + produtos)
 * Usa React Query para cache e refetch automático
 */
export function useCardapio() {
  return useQuery<CardapioResponse>({
    queryKey: ['cardapio'],
    queryFn: cardapioApi.getCardapioCompleto,
    staleTime: 5 * 60 * 1000, // 5 minutos
    refetchOnWindowFocus: true,
  });
}

/**
 * Hook para buscar produtos de uma categoria específica
 */
export function useProdutosPorCategoria(
  categoriaId: number,
  incluirIndisponiveis = false
) {
  return useQuery<Produto[]>({
    queryKey: ['produtos', 'categoria', categoriaId, incluirIndisponiveis],
    queryFn: () => cardapioApi.getProdutosPorCategoria(categoriaId, incluirIndisponiveis),
    staleTime: 5 * 60 * 1000,
    enabled: !!categoriaId,
  });
}

/**
 * Hook para buscar produtos por termo de busca
 */
export function useBuscaProdutos(termo: string) {
  return useQuery<Produto[]>({
    queryKey: ['produtos', 'busca', termo],
    queryFn: () => cardapioApi.buscarProdutos(termo),
    staleTime: 2 * 60 * 1000, // 2 minutos
    enabled: termo.length >= 2,
  });
}
