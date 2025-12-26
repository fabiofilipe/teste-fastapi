import { useState, useRef, useEffect } from 'react'
import Layout from '@/components/layout/Layout'
import CategoriaNav from '@/components/cardapio/CategoriaNav'
import ProdutoCard from '@/components/cardapio/ProdutoCard'
import Loading from '@/components/common/Loading'
import ErrorMessage from '@/components/common/ErrorMessage'
import { useCardapio } from '@/hooks/useCardapio'
import { useCarrinho } from '@/contexts/CarrinhoContext'
import type { Produto } from '@/types/cardapio.types'

function Cardapio() {
  const [categoriaAtiva, setCategoriaAtiva] = useState<number | undefined>(undefined)
  const produtosRef = useRef<HTMLDivElement>(null)

  // Hooks
  const { totalItens } = useCarrinho()
  const { data: cardapioData, isLoading, error, refetch } = useCardapio()

  // Scroll suave para a seção de produtos ao trocar categoria
  useEffect(() => {
    if (categoriaAtiva !== undefined && produtosRef.current) {
      // Pequeno delay para garantir que o conteúdo foi renderizado
      setTimeout(() => {
        produtosRef.current?.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        })
      }, 100)
    }
  }, [categoriaAtiva])

  // Handler para abrir modal de detalhes (será implementado no Sprint 4)
  const handleVerDetalhes = (produto: Produto) => {
    console.log('Ver detalhes do produto:', produto)
    // TODO: Abrir modal de customização (Sprint 4)
    alert(`Ver detalhes: ${produto.nome}\n\nModal de customização será implementado no Sprint 4.`)
  }

  // Handler para clicar no carrinho
  const handleCarrinhoClick = () => {
    console.log('Abrir carrinho')
    // TODO: Abrir sidebar do carrinho (Sprint 5)
    alert(`Carrinho: ${totalItens} itens\n\nSidebar do carrinho será implementado no Sprint 5.`)
  }

  // Loading state
  if (isLoading) {
    return (
      <Layout cartItemCount={totalItens} onCartClick={handleCarrinhoClick}>
        <Loading fullScreen size="lg" text="Carregando cardápio..." />
      </Layout>
    )
  }

  // Error state
  if (error) {
    return (
      <Layout cartItemCount={totalItens} onCartClick={handleCarrinhoClick}>
        <ErrorMessage
          variant="fullScreen"
          title="Erro ao carregar cardápio"
          message="Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente."
          onRetry={() => refetch()}
        />
      </Layout>
    )
  }

  // Sem dados
  if (!cardapioData?.categorias || cardapioData.categorias.length === 0) {
    return (
      <Layout cartItemCount={totalItens} onCartClick={handleCarrinhoClick}>
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">
              Nenhuma categoria encontrada
            </h2>
            <p className="text-gray-600">
              O cardápio está vazio no momento. Tente novamente mais tarde.
            </p>
          </div>
        </div>
      </Layout>
    )
  }

  // Filtrar categorias ativas
  const categoriasAtivas = cardapioData.categorias.filter((cat) => cat.ativa)

  // Produtos a serem exibidos (filtrados por categoria ou todos)
  let produtosExibidos: Produto[] = []

  if (categoriaAtiva === undefined) {
    // Mostrar todos os produtos de todas as categorias
    produtosExibidos = categoriasAtivas.flatMap((cat) => cat.produtos)
  } else {
    // Mostrar apenas produtos da categoria selecionada
    const categoriaEscolhida = categoriasAtivas.find((cat) => cat.id === categoriaAtiva)
    produtosExibidos = categoriaEscolhida?.produtos || []
  }

  // Filtrar apenas produtos disponíveis (opcional: pode mostrar indisponíveis também)
  // Vou manter todos os produtos, pois o ProdutoCard já lida com o estado de indisponível
  const produtosFiltrados = produtosExibidos

  return (
    <Layout
      cartItemCount={totalItens}
      onCartClick={handleCarrinhoClick}
      maxWidth="7xl"
    >
      <div className="py-6 space-y-6">
        {/* Header da página */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900">
            Nosso Cardápio
          </h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Escolha seus produtos favoritos e personalize como preferir
          </p>
        </div>

        {/* Navegação de Categorias */}
        <div className="sticky top-16 bg-white z-10 -mx-4 px-4 py-4 shadow-sm">
          <CategoriaNav
            categorias={categoriasAtivas}
            categoriaAtiva={categoriaAtiva}
            onCategoriaClick={(id) => {
              // Toggle: se clicar na categoria ativa, desseleciona
              setCategoriaAtiva(categoriaAtiva === id ? undefined : id)
            }}
          />
        </div>

        {/* Grid de Produtos */}
        <div ref={produtosRef} className="scroll-mt-24">
          {/* Título da seção */}
          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-gray-900">
              {categoriaAtiva === undefined
                ? 'Todos os Produtos'
                : categoriasAtivas.find((cat) => cat.id === categoriaAtiva)?.nome || 'Produtos'}
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              {produtosFiltrados.length}{' '}
              {produtosFiltrados.length === 1 ? 'produto encontrado' : 'produtos encontrados'}
            </p>
          </div>

          {/* Lista de produtos */}
          {produtosFiltrados.length === 0 ? (
            // Nenhum produto encontrado
            <div className="flex items-center justify-center min-h-[40vh]">
              <div className="text-center">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Nenhum produto encontrado
                </h3>
                <p className="text-gray-600">
                  Esta categoria não possui produtos disponíveis no momento.
                </p>
              </div>
            </div>
          ) : (
            // Grid de produtos
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {produtosFiltrados.map((produto) => (
                <ProdutoCard
                  key={produto.id}
                  produto={produto}
                  onVerDetalhes={handleVerDetalhes}
                />
              ))}
            </div>
          )}
        </div>

        {/* Footer informativo */}
        <div className="pt-12 pb-6 text-center border-t border-gray-200">
          <p className="text-sm text-gray-500">
            ✅ Sprint 3 - Etapa 3.3 completa
          </p>
          <p className="text-xs text-gray-400 mt-1">
            Navegação de Categorias • Grid de Produtos • Filtros Dinâmicos
          </p>
        </div>
      </div>
    </Layout>
  )
}

export default Cardapio
