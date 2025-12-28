import React, { useState } from 'react';
import { ShoppingCart, Pizza } from 'lucide-react';
import Layout from './components/layout/Layout';
import CarrinhoSidebar from './components/carrinho/CarrinhoSidebar';
import Button from './components/common/Button';
import { useCarrinho } from './contexts/CarrinhoContext';
import type { Produto, ProdutoVariacao, Ingrediente } from './types/cardapio.types';

const TestCarrinho: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const { adicionarItem, itens, totalItens, subtotal } = useCarrinho();

  // Dados mockados para testes
  const produtoMock: Produto = {
    id: 1,
    nome: 'Pizza Margherita',
    descricao: 'Molho de tomate, mussarela, tomate, manjericão e orégano',
    preco_base: 35.00,
    categoria_id: 1,
    imagem_url: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400',
    disponivel: true,
    personalizavel: true,
    variacoes: [
      { id: 1, produto_id: 1, tamanho: 'Pequena', preco: 25.00, disponivel: true },
      { id: 2, produto_id: 1, tamanho: 'Média', preco: 35.00, disponivel: true },
      { id: 3, produto_id: 1, tamanho: 'Grande', preco: 45.00, disponivel: true },
    ],
    ingredientes_padrao: [],
    ingredientes_adicionais_disponiveis: [],
  };

  const produtoMock2: Produto = {
    id: 2,
    nome: 'Pizza Calabresa',
    descricao: 'Molho de tomate, mussarela, calabresa e cebola',
    preco_base: 38.00,
    categoria_id: 1,
    imagem_url: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400',
    disponivel: true,
    personalizavel: true,
    variacoes: [
      { id: 4, produto_id: 2, tamanho: 'Média', preco: 38.00, disponivel: true },
      { id: 5, produto_id: 2, tamanho: 'Grande', preco: 48.00, disponivel: true },
    ],
    ingredientes_padrao: [],
    ingredientes_adicionais_disponiveis: [],
  };

  const ingredienteExtraMock: Ingrediente = {
    id: 1,
    nome: 'Bacon',
    tipo: 'EXTRA',
    preco_adicional: 5.00,
    disponivel: true,
  };

  const adicionarPizzaSimples = () => {
    adicionarItem({
      produto: produtoMock,
      variacao: produtoMock.variacoes[1], // Média
      quantidade: 1,
      ingredientesAdicionados: [],
      ingredientesRemovidos: [],
      preco_total: 35.00,
    });
    setIsSidebarOpen(true);
  };

  const adicionarPizzaComExtras = () => {
    adicionarItem({
      produto: produtoMock,
      variacao: produtoMock.variacoes[2], // Grande
      quantidade: 2,
      ingredientesAdicionados: [ingredienteExtraMock],
      ingredientesRemovidos: [],
      observacoes: 'Bem assada, por favor',
      preco_total: (45.00 + 5.00) * 2, // (base + extra) * quantidade
    });
    setIsSidebarOpen(true);
  };

  const adicionarCalabresa = () => {
    adicionarItem({
      produto: produtoMock2,
      variacao: produtoMock2.variacoes[1], // Grande
      quantidade: 1,
      ingredientesAdicionados: [],
      ingredientesRemovidos: [],
      preco_total: 48.00,
    });
    setIsSidebarOpen(true);
  };

  const formatarPreco = (valor: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(valor);
  };

  return (
    <Layout maxWidth="7xl">
      <div className="py-8">
        {/* Cabeçalho */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Teste do Carrinho de Compras
          </h1>
          <p className="text-gray-600">
            Teste da Etapa 5.1 - Sidebar do Carrinho
          </p>
        </div>

        {/* Status do Carrinho */}
        <div className="mb-8 p-6 bg-primary-50 rounded-lg border border-primary-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-2">
                Status do Carrinho
              </h2>
              <div className="space-y-1 text-sm text-gray-700">
                <p>
                  <span className="font-medium">Total de itens:</span> {totalItens}
                </p>
                <p>
                  <span className="font-medium">Subtotal:</span> {formatarPreco(subtotal)}
                </p>
                <p>
                  <span className="font-medium">Produtos únicos:</span> {itens.length}
                </p>
              </div>
            </div>
            <Button
              onClick={() => setIsSidebarOpen(true)}
              variant="primary"
              className="flex items-center gap-2"
            >
              <ShoppingCart className="w-5 h-5" />
              Abrir Carrinho
              {totalItens > 0 && (
                <span className="px-2 py-0.5 text-xs font-medium bg-white text-primary-600 rounded-full">
                  {totalItens}
                </span>
              )}
            </Button>
          </div>
        </div>

        {/* Cenários de Teste */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Cenários de Teste
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Cenário 1: Carrinho Vazio */}
            <div className="p-6 border border-gray-200 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-2">
                1. Carrinho Vazio
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Abrir sidebar sem itens no carrinho
              </p>
              <Button
                onClick={() => setIsSidebarOpen(true)}
                variant="outline"
                className="w-full"
              >
                Abrir Vazio
              </Button>
            </div>

            {/* Cenário 2: Pizza Simples */}
            <div className="p-6 border border-gray-200 rounded-lg bg-green-50 border-green-200">
              <div className="flex items-center gap-2 mb-2">
                <Pizza className="w-5 h-5 text-green-600" />
                <h3 className="font-semibold text-gray-900">
                  2. Pizza Simples
                </h3>
              </div>
              <p className="text-sm text-gray-600 mb-2">
                Margherita Média (1x)
              </p>
              <p className="text-xs text-gray-500 mb-4">
                Sem customizações
              </p>
              <Button
                onClick={adicionarPizzaSimples}
                variant="primary"
                className="w-full"
              >
                Adicionar
              </Button>
            </div>

            {/* Cenário 3: Pizza com Extras */}
            <div className="p-6 border border-gray-200 rounded-lg bg-blue-50 border-blue-200">
              <div className="flex items-center gap-2 mb-2">
                <Pizza className="w-5 h-5 text-blue-600" />
                <h3 className="font-semibold text-gray-900">
                  3. Pizza Customizada
                </h3>
              </div>
              <p className="text-sm text-gray-600 mb-2">
                Margherita Grande (2x)
              </p>
              <p className="text-xs text-gray-500 mb-4">
                + Bacon, Observações
              </p>
              <Button
                onClick={adicionarPizzaComExtras}
                variant="primary"
                className="w-full"
              >
                Adicionar
              </Button>
            </div>
          </div>
        </div>

        {/* Ações Rápidas */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Ações Rápidas
          </h2>
          <div className="flex flex-wrap gap-3">
            <Button onClick={adicionarPizzaSimples} variant="outline">
              + Margherita Média
            </Button>
            <Button onClick={adicionarCalabresa} variant="outline">
              + Calabresa Grande
            </Button>
            <Button onClick={adicionarPizzaComExtras} variant="outline">
              + Margherita Grande (2x) + Bacon
            </Button>
          </div>
        </div>

        {/* Funcionalidades Testadas */}
        <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Funcionalidades Implementadas
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-gray-900 mb-2">✅ Estrutura</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Drawer lateral direito</li>
                <li>• Overlay com backdrop</li>
                <li>• Portal (renderiza no body)</li>
                <li>• Responsivo (mobile-first)</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-2">✅ Animações</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Slide-in da direita</li>
                <li>• Fade-in do overlay</li>
                <li>• Transições suaves (300ms)</li>
                <li>• Estados hover/active</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-2">✅ Interações</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Fechar com botão X</li>
                <li>• Fechar com ESC</li>
                <li>• Fechar clicando no overlay</li>
                <li>• Bloqueia scroll do body</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-2">✅ Conteúdo</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Estado vazio (mensagem)</li>
                <li>• Lista de itens (básica)</li>
                <li>• Resumo (subtotal/total)</li>
                <li>• Botões de ação</li>
                <li>• Badge com contador</li>
                <li>• Limpar carrinho</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Notas */}
        <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-800">
            <strong>Nota:</strong> A Etapa 5.2 irá implementar o componente{' '}
            <code className="px-1 py-0.5 bg-yellow-100 rounded">CarrinhoItem</code>{' '}
            com layout detalhado, seletor de quantidade inline e botão de remover.
          </p>
        </div>
      </div>

      {/* CarrinhoSidebar */}
      <CarrinhoSidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />
    </Layout>
  );
};

export default TestCarrinho;
