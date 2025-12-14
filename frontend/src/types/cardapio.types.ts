export interface Ingrediente {
  id: number
  nome: string
  preco_adicional: number
  disponivel: boolean
}

export interface ProdutoIngrediente {
  ingrediente: Ingrediente
  obrigatorio: boolean
}

export interface ProdutoVariacao {
  id: number
  tamanho: string
  preco: number
  disponivel: boolean
}

export interface Produto {
  id: number
  nome: string
  descricao: string | null
  imagem_url: string | null
  categoria_id: number
  disponivel: boolean
  variacoes: ProdutoVariacao[]
  ingredientes: ProdutoIngrediente[]
}

export interface Categoria {
  id: number
  nome: string
  descricao: string | null
  icone: string | null
  ordem_exibicao: number
  ativa: boolean
  produtos: Produto[]
}

export interface CardapioResponse {
  categorias: Categoria[]
}

// Tipos para o carrinho
export interface ItemCarrinho {
  produto: Produto
  variacao: ProdutoVariacao
  quantidade: number
  ingredientesAdicionados: Ingrediente[]
  ingredientesRemovidos: number[]
  observacoes?: string
  preco_total: number
}

export interface Carrinho {
  itens: ItemCarrinho[]
  total: number
}
