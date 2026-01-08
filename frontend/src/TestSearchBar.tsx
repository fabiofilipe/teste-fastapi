import { useState } from 'react'
import SearchBar from '@/components/common/SearchBar'
import Layout from '@/components/layout/Layout'
import ProdutoModal from '@/components/cardapio/ProdutoModal'
import type { Produto } from '@/types/cardapio.types'
import { useCarrinho } from '@/contexts/CarrinhoContext'

function TestSearchBar() {
    const [produtoSelecionado, setProdutoSelecionado] = useState<Produto | null>(null)
    const { adicionarItem } = useCarrinho()

    const handleSelectProduct = (produto: Produto) => {
        console.log('Produto selecionado:', produto)
        setProdutoSelecionado(produto)
    }

    const handleCloseModal = () => {
        setProdutoSelecionado(null)
    }

    const handleAddToCart = (
        produto: Produto,
        variacao: any,
        customizacao: any,
        quantidade: number
    ) => {
        // Adicionar ao carrinho (preco_total é calculado automaticamente)
        adicionarItem({
            produto,
            variacao,
            quantidade,
            ingredientesAdicionados: customizacao.ingredientesAdicionados,
            ingredientesRemovidos: customizacao.ingredientesRemovidos,
            observacoes: customizacao.observacoes,
        })

        // Fechar modal
        handleCloseModal()

        // Feedback
        console.log('Produto adicionado ao carrinho:', {
            produto: produto.nome,
            tamanho: variacao.tamanho,
            quantidade,
        })
    }

    return (
        <Layout maxWidth="7xl">
            <div className="py-8 space-y-8">
                {/* Cabeçalho */}
                <div className="text-center">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">
                        Teste de Busca de Produtos
                    </h1>
                    <p className="text-gray-600">
                        Digite pelo menos 2 caracteres para buscar produtos
                    </p>
                </div>

                {/* Cenário 1: SearchBar padrão */}
                <section className="space-y-4">
                    <div className="border-b pb-2">
                        <h2 className="text-xl font-semibold text-gray-900">
                            Cenário 1: Busca Padrão
                        </h2>
                        <p className="text-sm text-gray-600">
                            Busca com placeholder padrão e seleção de produto
                        </p>
                    </div>

                    <SearchBar
                        onSelectProduct={handleSelectProduct}
                        onClose={() => console.log('Busca fechada')}
                    />
                </section>

                {/* Cenário 2: SearchBar com autoFocus */}
                <section className="space-y-4">
                    <div className="border-b pb-2">
                        <h2 className="text-xl font-semibold text-gray-900">
                            Cenário 2: Com AutoFocus
                        </h2>
                        <p className="text-sm text-gray-600">
                            Campo de busca com foco automático ao carregar
                        </p>
                    </div>

                    <SearchBar
                        onSelectProduct={handleSelectProduct}
                        placeholder="Digite aqui para buscar pizzas..."
                        autoFocus={true}
                        className="max-w-2xl mx-auto"
                    />
                </section>

                {/* Cenário 3: SearchBar customizado */}
                <section className="space-y-4">
                    <div className="border-b pb-2">
                        <h2 className="text-xl font-semibold text-gray-900">
                            Cenário 3: Busca Customizada
                        </h2>
                        <p className="text-sm text-gray-600">
                            Busca com placeholder customizado e container limitado
                        </p>
                    </div>

                    <div className="max-w-md mx-auto">
                        <SearchBar
                            onSelectProduct={handleSelectProduct}
                            placeholder="Busque sua pizza favorita..."
                            className="shadow-lg"
                        />
                    </div>
                </section>

                {/* Instruções */}
                <section className="bg-blue-50 border border-blue-200 rounded-lg p-6 space-y-3">
                    <h3 className="text-lg font-semibold text-blue-900 flex items-center gap-2">
                        <span className="text-2xl">ℹ️</span>
                        Instruções de Teste
                    </h3>

                    <div className="space-y-2 text-sm text-blue-800">
                        <p className="font-medium">✅ Funcionalidades para testar:</p>
                        <ul className="list-disc list-inside space-y-1 ml-4">
                            <li>
                                <strong>Debounce:</strong> Digite rapidamente e note que a busca
                                aguarda 300ms após parar de digitar
                            </li>
                            <li>
                                <strong>Mínimo 2 caracteres:</strong> A busca só é ativada com 2+
                                caracteres
                            </li>
                            <li>
                                <strong>Destaque de termos:</strong> O termo buscado aparece
                                destacado em amarelo nos resultados
                            </li>
                            <li>
                                <strong>Navegação por teclado:</strong> Use setas ↑↓ para navegar,
                                Enter para selecionar, Esc para fechar
                            </li>
                            <li>
                                <strong>Click fora:</strong> Clique fora do dropdown para fechá-lo
                            </li>
                            <li>
                                <strong>Botão limpar:</strong> Clique no X para limpar a busca
                            </li>
                            <li>
                                <strong>Loading state:</strong> Veja o spinner enquanto carrega
                            </li>
                            <li>
                                <strong>Resultados vazios:</strong> Busque por algo que não existe
                                (ex: "xyzabc")
                            </li>
                            <li>
                                <strong>Seleção de produto:</strong> Clique em um resultado para
                                abrir o modal
                            </li>
                        </ul>

                        <p className="font-medium mt-4">🔍 Termos sugeridos para testar:</p>
                        <ul className="list-disc list-inside space-y-1 ml-4">
                            <li>
                                <code className="bg-blue-100 px-2 py-0.5 rounded">pizza</code> -
                                deve retornar produtos de pizza
                            </li>
                            <li>
                                <code className="bg-blue-100 px-2 py-0.5 rounded">marg</code> -
                                teste substring (ex: Margherita)
                            </li>
                            <li>
                                <code className="bg-blue-100 px-2 py-0.5 rounded">calaba</code> -
                                teste produto específico
                            </li>
                            <li>
                                <code className="bg-blue-100 px-2 py-0.5 rounded">beb</code> - teste
                                categoria diferente
                            </li>
                            <li>
                                <code className="bg-blue-100 px-2 py-0.5 rounded">xyzabc</code> -
                                teste sem resultados
                            </li>
                        </ul>
                    </div>
                </section>

                {/* Log de eventos */}
                <section className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <h3 className="text-sm font-semibold text-gray-700 mb-2">
                        📋 Console Log
                    </h3>
                    <p className="text-xs text-gray-600">
                        Abra o console do navegador (F12) para ver logs de eventos:
                        <br />
                        - Produto selecionado
                        <br />
                        - Busca fechada
                        <br />- Produto adicionado ao carrinho
                    </p>
                </section>
            </div>

            {/* Modal de produto */}
            {produtoSelecionado && (
                <ProdutoModal
                    produto={produtoSelecionado}
                    isOpen={!!produtoSelecionado}
                    onClose={handleCloseModal}
                    onAddToCart={handleAddToCart}
                />
            )}
        </Layout>
    )
}

export default TestSearchBar
