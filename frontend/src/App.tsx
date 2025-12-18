import { useState } from 'react'
import { Search, ShoppingCart, Plus, Trash2 } from 'lucide-react'
import Layout from './components/layout/Layout'
import Button from './components/common/Button'
import Badge from './components/common/Badge'
import Card from './components/common/Card'
import Loading from './components/common/Loading'
import ErrorMessage from './components/common/ErrorMessage'
import { CarrinhoProvider, useCarrinho } from './contexts/CarrinhoContext'

// ============================================================================
// APP CONTENT (usa o hook useCarrinho)
// ============================================================================

function AppContent() {
  const [isLoading, setIsLoading] = useState(false)
  const [showError, setShowError] = useState(false)

  // Hook do carrinho
  const { totalItens, subtotal, adicionarItem, removerItem, limparCarrinho, itens } = useCarrinho()

  const handleLoadingTest = () => {
    setIsLoading(true)
    setTimeout(() => setIsLoading(false), 2000)
  }

  // ============================================================================
  // FUNÇÕES HELPER PARA TESTE DO CARRINHO
  // ============================================================================

  const adicionarPizzaTeste = () => {
    adicionarItem({
      produto: {
        id: 1,
        nome: 'Pizza Margherita',
        descricao: 'Molho de tomate, mussarela e manjericão',
        disponivel: true,
        categoria_id: 1,
        variacoes: [],
        ingredientes_padrao: [],
      },
      variacao: {
        id: 1,
        produto_id: 1,
        tamanho: 'MEDIA',
        preco: 35.90,
        disponivel: true,
      },
      quantidade: 1,
      ingredientesAdicionados: [
        {
          id: 10,
          nome: 'Borda recheada',
          descricao: 'Borda recheada com catupiry',
          preco_adicional: 8.00,
          disponivel: true,
        },
      ],
      ingredientesRemovidos: [],
      observacoes: 'Sem cebola, por favor',
    })
  }

  return (
    <Layout
      cartItemCount={totalItens}
      onCartClick={() => alert(`Carrinho: ${totalItens} itens (R$ ${subtotal.toFixed(2)})`)}
      onLogoClick={() => alert('Logo clicado - voltando ao início')}
    >
      <div className="space-y-8">
        {/* Header da página de testes */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-gray-900">Componentes Base + Layout + Carrinho</h1>
          <p className="text-gray-600">Etapas 2.1, 2.2 e 2.3 - Sprint 2</p>
          <div className="flex justify-center gap-2 mt-4">
            <Badge variant="success">{totalItens} itens</Badge>
            <Badge variant="info">R$ {subtotal.toFixed(2)}</Badge>
          </div>
        </div>

        {/* Teste do Carrinho Context */}
        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Context do Carrinho (Etapa 2.3)</h2>
          <Card>
            <div className="space-y-4">
              <div className="flex flex-wrap gap-2">
                <Button
                  variant="primary"
                  leftIcon={<Plus size={16} />}
                  onClick={adicionarPizzaTeste}
                >
                  Adicionar Pizza Teste
                </Button>
                <Button
                  variant="danger"
                  leftIcon={<Trash2 size={16} />}
                  onClick={limparCarrinho}
                  disabled={itens.length === 0}
                >
                  Limpar Carrinho
                </Button>
              </div>

              <div className="border-t border-gray-200 pt-4">
                <p className="text-sm font-medium text-gray-700 mb-2">Itens no carrinho:</p>
                {itens.length === 0 ? (
                  <p className="text-sm text-gray-500 italic">Carrinho vazio</p>
                ) : (
                  <div className="space-y-2">
                    {itens.map((item) => (
                      <div
                        key={item.id}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                      >
                        <div className="flex-1">
                          <p className="font-medium text-gray-900">
                            {item.produto.nome} ({item.variacao.tamanho})
                          </p>
                          <p className="text-sm text-gray-600">
                            Quantidade: {item.quantidade} • R$ {item.preco_total.toFixed(2)}
                          </p>
                          {item.ingredientesAdicionados.length > 0 && (
                            <p className="text-xs text-gray-500">
                              + {item.ingredientesAdicionados.map((ing) => ing.nome).join(', ')}
                            </p>
                          )}
                          {item.observacoes && (
                            <p className="text-xs text-gray-500 italic">"{item.observacoes}"</p>
                          )}
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removerItem(item.id)}
                        >
                          <Trash2 size={16} />
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="border-t border-gray-200 pt-4">
                <div className="flex justify-between items-center">
                  <p className="text-lg font-semibold text-gray-900">Total:</p>
                  <div className="text-right">
                    <p className="text-sm text-gray-600">{totalItens} itens</p>
                    <p className="text-2xl font-bold text-primary-600">
                      R$ {subtotal.toFixed(2)}
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm text-blue-800">
                  <strong>✅ Funcionalidades testadas:</strong>
                </p>
                <ul className="text-xs text-blue-700 mt-2 space-y-1 ml-4 list-disc">
                  <li>Adicionar item ao carrinho (com ingredientes adicionais)</li>
                  <li>Remover item específico</li>
                  <li>Limpar carrinho completo</li>
                  <li>Cálculo automático de preços</li>
                  <li>Persistência em localStorage</li>
                  <li>Badge do carrinho atualiza automaticamente</li>
                </ul>
              </div>
            </div>
          </Card>
        </section>

        {/* Buttons */}
        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Buttons</h2>
          <Card>
            <div className="space-y-4">
              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Variantes:</p>
                <div className="flex flex-wrap gap-2">
                  <Button variant="primary">Primary</Button>
                  <Button variant="secondary">Secondary</Button>
                  <Button variant="outline">Outline</Button>
                  <Button variant="ghost">Ghost</Button>
                  <Button variant="danger">Danger</Button>
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Tamanhos:</p>
                <div className="flex flex-wrap gap-2 items-center">
                  <Button size="sm">Small</Button>
                  <Button size="md">Medium</Button>
                  <Button size="lg">Large</Button>
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Com ícones:</p>
                <div className="flex flex-wrap gap-2">
                  <Button leftIcon={<Search size={16} />}>Buscar</Button>
                  <Button variant="secondary" rightIcon={<ShoppingCart size={16} />}>
                    Carrinho
                  </Button>
                  <Button variant="outline" leftIcon={<Plus size={16} />}>
                    Adicionar
                  </Button>
                  <Button variant="danger" leftIcon={<Trash2 size={16} />}>
                    Remover
                  </Button>
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Estados:</p>
                <div className="flex flex-wrap gap-2">
                  <Button isLoading onClick={handleLoadingTest}>Loading</Button>
                  <Button disabled>Disabled</Button>
                  <Button variant="primary" isLoading>
                    Processando...
                  </Button>
                </div>
              </div>
            </div>
          </Card>
        </section>

        {/* Badges */}
        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Badges</h2>
          <Card>
            <div className="space-y-4">
              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Variantes:</p>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="success">Disponível</Badge>
                  <Badge variant="warning">Estoque Baixo</Badge>
                  <Badge variant="error">Esgotado</Badge>
                  <Badge variant="info">Novo</Badge>
                  <Badge variant="neutral">Tag</Badge>
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Tamanhos:</p>
                <div className="flex flex-wrap gap-2 items-center">
                  <Badge size="sm">Small</Badge>
                  <Badge size="md">Medium</Badge>
                  <Badge size="lg">Large</Badge>
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Com dot:</p>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="success" dot>3 itens</Badge>
                  <Badge variant="info" dot>Em preparo</Badge>
                  <Badge variant="error" dot>Cancelado</Badge>
                </div>
              </div>
            </div>
          </Card>
        </section>

        {/* Cards */}
        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Cards</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card variant="default">
              <h3 className="font-semibold text-gray-900 mb-2">Card Padrão</h3>
              <p className="text-gray-600 text-sm">
                Card com sombra sutil e estilo padrão.
              </p>
            </Card>

            <Card variant="interactive" hoverable>
              <h3 className="font-semibold text-gray-900 mb-2">Card Interativo</h3>
              <p className="text-gray-600 text-sm">
                Passe o mouse para ver o efeito de elevação.
              </p>
            </Card>

            <Card variant="outlined" padding="lg">
              <h3 className="font-semibold text-gray-900 mb-2">Card Outlined</h3>
              <p className="text-gray-600 text-sm">
                Card apenas com borda, sem sombra.
              </p>
            </Card>
          </div>
        </section>

        {/* Loading */}
        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Loading</h2>
          <Card>
            <div className="space-y-6">
              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Variantes:</p>
                <div className="flex flex-wrap gap-8 items-center">
                  <div className="text-center">
                    <Loading variant="spinner" size="md" />
                    <p className="text-xs text-gray-500 mt-2">Spinner</p>
                  </div>
                  <div className="text-center">
                    <Loading variant="dots" size="md" />
                    <p className="text-xs text-gray-500 mt-2">Dots</p>
                  </div>
                  <div className="text-center">
                    <Loading variant="pulse" size="md" />
                    <p className="text-xs text-gray-500 mt-2">Pulse</p>
                  </div>
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Tamanhos:</p>
                <div className="flex flex-wrap gap-8 items-center">
                  <Loading size="sm" text="Small" />
                  <Loading size="md" text="Medium" />
                  <Loading size="lg" text="Large" />
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Full Screen (teste):</p>
                <Button onClick={handleLoadingTest}>
                  Testar Loading Full Screen
                </Button>
              </div>
            </div>
          </Card>
        </section>

        {/* Error Messages */}
        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Error Messages</h2>
          <div className="space-y-4">
            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">Inline:</p>
              <ErrorMessage
                variant="inline"
                message="Email inválido"
              />
            </div>

            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">Card (sem retry):</p>
              <ErrorMessage
                variant="card"
                title="Erro ao processar"
                message="Não foi possível processar sua solicitação."
              />
            </div>

            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">Card (com retry):</p>
              <ErrorMessage
                variant="card"
                title="Erro ao carregar cardápio"
                message="Não foi possível conectar ao servidor. Tente novamente."
                onRetry={() => alert('Tentando novamente...')}
              />
            </div>

            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">Full Screen (teste):</p>
              <Button onClick={() => setShowError(true)}>
                Testar Error Full Screen
              </Button>
            </div>
          </div>
        </section>

        {/* Layout Test - Scroll */}
        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Teste de Layout (Scroll)</h2>
          <p className="text-gray-600 mb-4">
            Role a página para baixo para ver o Header fixo no topo e o Footer no final.
          </p>
          <div className="space-y-4">
            {Array.from({ length: 10 }).map((_, i) => (
              <Card key={i}>
                <h3 className="font-semibold text-gray-900 mb-2">Card de Teste #{i + 1}</h3>
                <p className="text-gray-600 text-sm">
                  Este card está aqui para testar o scroll da página. O Header deve permanecer fixo no topo.
                </p>
              </Card>
            ))}
          </div>
        </section>

        {/* Footer */}
        <div className="text-center pt-8 pb-4 text-gray-500 text-sm border-t border-gray-200">
          <p>✅ Etapas 2.1, 2.2 e 2.3 completas</p>
          <p className="text-xs mt-1">Header fixo • Footer no final • Layout responsivo • Context do Carrinho</p>
        </div>
      </div>

      {/* Loading Full Screen */}
      {isLoading && (
        <Loading
          fullScreen
          size="lg"
          text="Carregando..."
          variant="spinner"
        />
      )}

      {/* Error Full Screen */}
      {showError && (
        <ErrorMessage
          variant="fullScreen"
          title="Ops! Algo deu errado"
          message="Não foi possível conectar ao servidor. Verifique sua conexão."
          onRetry={() => setShowError(false)}
        />
      )}
    </Layout>
  )
}

// ============================================================================
// APP WRAPPER (com CarrinhoProvider)
// ============================================================================

function App() {
  return (
    <CarrinhoProvider>
      <AppContent />
    </CarrinhoProvider>
  )
}

export default App
