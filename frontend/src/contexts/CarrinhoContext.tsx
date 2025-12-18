import { createContext, useContext, useState, useEffect, useMemo } from 'react';
import type { ReactNode } from 'react';
import type { Produto, ProdutoVariacao, Ingrediente } from '@/types/cardapio.types';

// ============================================================================
// TYPES & INTERFACES
// ============================================================================

export interface ItemCarrinho {
  id: string;
  produto: Produto;
  variacao: ProdutoVariacao;
  quantidade: number;
  ingredientesAdicionados: Ingrediente[];
  ingredientesRemovidos: number[];
  observacoes?: string;
  preco_total: number;
}

export interface CarrinhoContextType {
  itens: ItemCarrinho[];
  adicionarItem: (item: Omit<ItemCarrinho, 'id'>) => void;
  removerItem: (id: string) => void;
  atualizarQuantidade: (id: string, quantidade: number) => void;
  limparCarrinho: () => void;
  totalItens: number;
  subtotal: number;
}

// ============================================================================
// CONTEXT
// ============================================================================

const CarrinhoContext = createContext<CarrinhoContextType | undefined>(undefined);

const CARRINHO_STORAGE_KEY = 'pizzaria:carrinho';

// ============================================================================
// PROVIDER
// ============================================================================

interface CarrinhoProviderProps {
  children: ReactNode;
}

export function CarrinhoProvider({ children }: CarrinhoProviderProps) {
  const [itens, setItens] = useState<ItemCarrinho[]>([]);
  const [isInitialized, setIsInitialized] = useState(false);

  // ============================================================================
  // LOAD FROM LOCALSTORAGE (on mount)
  // ============================================================================

  useEffect(() => {
    try {
      const storedCarrinho = localStorage.getItem(CARRINHO_STORAGE_KEY);
      if (storedCarrinho) {
        const parsed = JSON.parse(storedCarrinho);
        setItens(Array.isArray(parsed) ? parsed : []);
      }
    } catch (error) {
      console.error('Erro ao carregar carrinho do localStorage:', error);
      setItens([]);
    } finally {
      setIsInitialized(true);
    }
  }, []);

  // ============================================================================
  // SAVE TO LOCALSTORAGE (on itens change)
  // ============================================================================

  useEffect(() => {
    if (!isInitialized) return;

    try {
      localStorage.setItem(CARRINHO_STORAGE_KEY, JSON.stringify(itens));
    } catch (error) {
      console.error('Erro ao salvar carrinho no localStorage:', error);
    }
  }, [itens, isInitialized]);

  // ============================================================================
  // HELPER FUNCTIONS
  // ============================================================================

  /**
   * Calcula o preço total de um item considerando:
   * - Preço base da variação
   * - Ingredientes adicionados
   * - Quantidade
   */
  const calcularPrecoItem = (
    variacao: ProdutoVariacao,
    ingredientesAdicionados: Ingrediente[],
    quantidade: number
  ): number => {
    const precoBase = variacao.preco;
    const precoIngredientes = ingredientesAdicionados.reduce(
      (total, ing) => total + ing.preco_adicional,
      0
    );
    return (precoBase + precoIngredientes) * quantidade;
  };

  // ============================================================================
  // CARRINHO ACTIONS
  // ============================================================================

  /**
   * Adiciona um novo item ao carrinho
   */
  const adicionarItem = (itemData: Omit<ItemCarrinho, 'id'>) => {
    const novoItem: ItemCarrinho = {
      id: crypto.randomUUID(),
      ...itemData,
      preco_total: calcularPrecoItem(
        itemData.variacao,
        itemData.ingredientesAdicionados,
        itemData.quantidade
      ),
    };

    setItens((prevItens) => [...prevItens, novoItem]);
  };

  /**
   * Remove um item do carrinho pelo ID
   */
  const removerItem = (id: string) => {
    setItens((prevItens) => prevItens.filter((item) => item.id !== id));
  };

  /**
   * Atualiza a quantidade de um item específico
   */
  const atualizarQuantidade = (id: string, quantidade: number) => {
    if (quantidade <= 0) {
      removerItem(id);
      return;
    }

    setItens((prevItens) =>
      prevItens.map((item) => {
        if (item.id !== id) return item;

        return {
          ...item,
          quantidade,
          preco_total: calcularPrecoItem(
            item.variacao,
            item.ingredientesAdicionados,
            quantidade
          ),
        };
      })
    );
  };

  /**
   * Remove todos os itens do carrinho
   */
  const limparCarrinho = () => {
    setItens([]);
  };

  // ============================================================================
  // COMPUTED VALUES
  // ============================================================================

  /**
   * Número total de itens no carrinho (soma das quantidades)
   */
  const totalItens = useMemo(() => {
    return itens.reduce((total, item) => total + item.quantidade, 0);
  }, [itens]);

  /**
   * Valor total do carrinho (soma de todos os preços)
   */
  const subtotal = useMemo(() => {
    return itens.reduce((total, item) => total + item.preco_total, 0);
  }, [itens]);

  // ============================================================================
  // CONTEXT VALUE
  // ============================================================================

  const value: CarrinhoContextType = {
    itens,
    adicionarItem,
    removerItem,
    atualizarQuantidade,
    limparCarrinho,
    totalItens,
    subtotal,
  };

  return <CarrinhoContext.Provider value={value}>{children}</CarrinhoContext.Provider>;
}

// ============================================================================
// CUSTOM HOOK
// ============================================================================

/**
 * Hook para acessar o contexto do carrinho
 * @throws Error se usado fora do CarrinhoProvider
 */
export function useCarrinho() {
  const context = useContext(CarrinhoContext);

  if (context === undefined) {
    throw new Error('useCarrinho deve ser usado dentro de um CarrinhoProvider');
  }

  return context;
}
