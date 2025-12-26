import { useState } from 'react'
import Layout from '@/components/layout/Layout'
import Card from '@/components/common/Card'
import Button from '@/components/common/Button'
import ProdutoModal from '@/components/cardapio/ProdutoModal'
import VariacaoSelector from '@/components/cardapio/VariacaoSelector'
import type { Produto, ProdutoVariacao } from '@/types/cardapio.types'
import { Pizza } from 'lucide-react'

// Dados de teste
const produtosMock: Produto[] = [
  {
    id: 1,
    nome: 'Pizza Margherita',
    descricao: 'Molho de tomate, mussarela de búfala, manjericão fresco e azeite extra virgem',
    imagem_url: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&h=400&fit=crop',
    categoria_id: 1,
    disponivel: true,
    variacoes: [
      { id: 1, tamanho: 'Pequena (4 fatias)', preco: 25.9, disponivel: true },
      { id: 2, tamanho: 'Média (6 fatias)', preco: 35.9, disponivel: true },
      { id: 3, tamanho: 'Grande (8 fatias)', preco: 45.9, disponivel: true },
      { id: 4, tamanho: 'Gigante (12 fatias)', preco: 55.9, disponivel: true },
    ],
    ingredientes: [
      {
        ingrediente: { id: 1, nome: 'Mussarela de búfala', preco_adicional: 0, disponivel: true },
        obrigatorio: true,
      },
      {
        ingrediente: { id: 2, nome: 'Manjericão', preco_adicional: 0, disponivel: true },
        obrigatorio: true,
      },
    ],
  },
  {
    id: 2,
    nome: 'Pizza Calabresa Premium',
    descricao: 'Calabresa artesanal, cebola roxa, azeitona preta e mussarela especial',
    imagem_url: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=600&h=400&fit=crop',
    categoria_id: 1,
    disponivel: true,
    variacoes: [
      { id: 5, tamanho: 'Média (6 fatias)', preco: 38.9, disponivel: true },
      { id: 6, tamanho: 'Grande (8 fatias)', preco: 48.9, disponivel: true },
      { id: 7, tamanho: 'Gigante (12 fatias)', preco: 58.9, disponivel: false },
    ],
    ingredientes: [
      {
        ingrediente: { id: 3, nome: 'Calabresa artesanal', preco_adicional: 0, disponivel: true },
        obrigatorio: true,
      },
      {
        ingrediente: { id: 4, nome: 'Cebola roxa', preco_adicional: 2, disponivel: true },
        obrigatorio: false,
      },
    ],
  },
  {
    id: 3,
    nome: 'Pizza Quatro Queijos',
    descricao: 'Mussarela, provolone, parmesão e gorgonzola',
    imagem_url: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&h=400&fit=crop',
    categoria_id: 1,
    disponivel: true,
    variacoes: [
      { id: 8, tamanho: 'Grande (8 fatias)', preco: 49.9, disponivel: true },
    ],
    ingredientes: [],
  },
  {
    id: 4,
    nome: 'Pizza Portuguesa (Indisponível)',
    descricao: 'Presunto, ovos, cebola, azeitona, ervilha e mussarela',
    imagem_url: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&h=400&fit=crop',
    categoria_id: 1,
    disponivel: false,
    variacoes: [
      { id: 9, tamanho: 'Grande (8 fatias)', preco: 52.9, disponivel: false },
    ],
    ingredientes: [],
  },
]

function TestVariacao() {
  // Estado para controlar qual modal está aberto
  const [produtoSelecionado, setProdutoSelecionado] = useState<Produto | null>(null)

  // Estado para teste standalone do VariacaoSelector
  const [variacaoStandalone, setVariacaoStandalone] = useState<ProdutoVariacao | null>(null)

  // Handler para adicionar ao carrinho
  const handleAddToCart = (
    produto: Produto,
    variacao: ProdutoVariacao,
    customizacao: {
      ingredientesAdicionados: any[]
      ingredientesRemovidos: number[]
      observacoes: string
      precoIngredientes: number
    },
    quantidade: number
  ) => {
    const precoUnitario = variacao.preco + customizacao.precoIngredientes
    const precoTotal = precoUnitario * quantidade

    let mensagem =
      `Produto adicionado ao carrinho!\n\n` +
      `📦 Produto: ${produto.nome}\n` +
      `📏 Tamanho: ${variacao.tamanho}\n` +
      `💰 Preço base: R$ ${variacao.preco.toFixed(2)}\n`

    if (customizacao.ingredientesAdicionados.length > 0) {
      mensagem += `\n✨ Ingredientes adicionados:\n`
      customizacao.ingredientesAdicionados.forEach((ing) => {
        mensagem += `  • ${ing.nome} (+R$ ${ing.preco_adicional.toFixed(2)})\n`
      })
    }

    if (customizacao.ingredientesRemovidos.length > 0) {
      mensagem += `\n❌ Ingredientes removidos: ${customizacao.ingredientesRemovidos.length}\n`
    }

    if (customizacao.observacoes) {
      mensagem += `\n📝 Observações: ${customizacao.observacoes}\n`
    }

    if (customizacao.precoIngredientes > 0) {
      mensagem += `\n💵 Ingredientes extras: +R$ ${customizacao.precoIngredientes.toFixed(2)}\n`
    }

    if (quantidade > 1) {
      mensagem += `\n📊 Subtotal unitário: R$ ${precoUnitario.toFixed(2)}\n`
      mensagem += `📦 Quantidade: × ${quantidade}\n`
    }

    mensagem += `\n🎯 TOTAL: R$ ${precoTotal.toFixed(2)}`

    alert(mensagem)
  }

  return (
    <Layout maxWidth="7xl">
      <div className="py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Teste: Modal de Produto Completo
          </h1>
          <p className="text-gray-600">
            Etapas 4.2 + 4.3 - Testando VariacaoSelector, IngredientesCustomizacao e ProdutoModal
          </p>
        </div>

        {/* Teste Standalone do VariacaoSelector */}
        <Card className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Teste 1: VariacaoSelector Standalone
          </h2>
          <p className="text-sm text-gray-600 mb-4">
            Componente isolado do seletor de variações (layout vertical)
          </p>
          <VariacaoSelector
            variacoes={produtosMock[0].variacoes}
            variacaoSelecionada={variacaoStandalone?.id}
            onChange={setVariacaoStandalone}
          />
          {variacaoStandalone && (
            <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm text-green-800">
                <strong>Selecionado:</strong> {variacaoStandalone.tamanho} - R${' '}
                {variacaoStandalone.preco.toFixed(2)}
              </p>
            </div>
          )}
        </Card>

        {/* Teste do ProdutoModal com diferentes produtos */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Teste 2: ProdutoModal Completo
          </h2>
          <p className="text-sm text-gray-600 mb-4">
            Clique em um produto para abrir o modal de customização
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {produtosMock.map((produto) => (
              <Card
                key={produto.id}
                variant="interactive"
                hoverable={produto.disponivel}
                className="overflow-hidden"
              >
                <div className="relative aspect-square overflow-hidden bg-gray-100 -mx-4 -mt-4 mb-3">
                  <img
                    src={produto.imagem_url || ''}
                    alt={produto.nome}
                    className="w-full h-full object-cover"
                  />
                  {!produto.disponivel && (
                    <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
                      <span className="text-white font-semibold text-sm">
                        Indisponível
                      </span>
                    </div>
                  )}
                </div>
                <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                  {produto.nome}
                </h3>
                <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                  {produto.descricao}
                </p>
                <Button
                  variant={produto.disponivel ? 'primary' : 'outline'}
                  size="sm"
                  onClick={() => setProdutoSelecionado(produto)}
                  disabled={!produto.disponivel}
                  className="w-full"
                  leftIcon={<Pizza size={16} />}
                >
                  {produto.disponivel ? 'Ver Detalhes' : 'Indisponível'}
                </Button>
              </Card>
            ))}
          </div>
        </div>

        {/* Informações sobre os cenários testados */}
        <Card>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Cenários Testados:
          </h2>
          <div className="space-y-3 text-sm text-gray-700">
            <div className="flex gap-3">
              <span className="font-semibold text-gray-900 min-w-[180px]">
                Pizza Margherita:
              </span>
              <span>4 variações disponíveis (R$ 25,90 - R$ 55,90) + 2 ingredientes customizáveis</span>
            </div>
            <div className="flex gap-3">
              <span className="font-semibold text-gray-900 min-w-[180px]">
                Pizza Calabresa:
              </span>
              <span>3 variações (1 indisponível) + 2 ingredientes customizáveis</span>
            </div>
            <div className="flex gap-3">
              <span className="font-semibold text-gray-900 min-w-[180px]">
                Pizza Quatro Queijos:
              </span>
              <span>1 variação disponível (preço fixo R$ 49,90) + sem customização</span>
            </div>
            <div className="flex gap-3">
              <span className="font-semibold text-gray-900 min-w-[180px]">
                Pizza Portuguesa:
              </span>
              <span>Produto completamente indisponível (teste de estado desabilitado)</span>
            </div>
          </div>
        </Card>

        {/* Features testadas */}
        <Card className="mt-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Features Implementadas (Etapas 4.2 + 4.3):
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Seletor com radio buttons customizados</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Tamanho e preço de cada variação exibidos</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Preço base atualiza ao selecionar variação</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Ingredientes padrão (obrigatórios e opcionais)</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Remover ingredientes opcionais (checkbox)</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Adicionar ingredientes extras (8 opções disponíveis)</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Preço adicional de cada ingrediente exibido</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Cálculo de preço em tempo real (base + extras)</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Campo de observações (200 caracteres)</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Resumo detalhado do preço total</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Estados visuais (hover, selected, removed, added)</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span className="text-gray-700">Alert detalhado ao adicionar ao carrinho</span>
            </div>
          </div>
        </Card>

        {/* Próximas etapas */}
        <Card className="mt-6 bg-blue-50 border-blue-200">
          <h2 className="text-xl font-semibold text-blue-900 mb-4">
            Próxima Etapa:
          </h2>
          <div className="space-y-2 text-sm text-blue-800">
            <div className="flex items-start gap-2">
              <span className="font-bold">⏳</span>
              <span>
                <strong>Etapa 4.4:</strong> Resumo e Adicionar ao Carrinho (seletor de quantidade e integração final com carrinho)
              </span>
            </div>
          </div>
        </Card>
      </div>

      {/* Modal de Produto */}
      <ProdutoModal
        isOpen={!!produtoSelecionado}
        onClose={() => setProdutoSelecionado(null)}
        produto={produtoSelecionado}
        onAddToCart={handleAddToCart}
      />
    </Layout>
  )
}

export default TestVariacao
