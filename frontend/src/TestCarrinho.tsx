import React, { useState } from 'react';
import { ShoppingCart, Pizza } from 'lucide-react';
import Layout from './components/layout/Layout';
import CarrinhoSidebar from './components/carrinho/CarrinhoSidebar';
import Button from './components/common/Button';
import { useCarrinho } from './contexts/CarrinhoContext';
import type { Produto, Ingrediente } from './types/cardapio.types';

const TestCarrinho: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const { adicionarItem, itens, totalItens, subtotal } = useCarrinho();

  // Dados mockados para testes
  const produtoMock: Produto = {
    id: 1,
    nome: 'Pizza Margherita',
    descricao: 'Molho de tomate, mussarela, tomate, manjericão e orégano',
    imagem_url: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400',
    categoria_id: 1,
    disponivel: true,
    variacoes: [
      { id: 1, tamanho: 'Pequena', preco: 25.00, disponivel: true },
      { id: 2, tamanho: 'Média', preco: 35.00, disponivel: true },
      { id: 3, tamanho: 'Grande', preco: 45.00, disponivel: true },
    ],
    ingredientes: [],
  };

  const produtoMock2: Produto = {
    id: 2,
    nome: 'Pizza Calabresa',
    descricao: 'Molho de tomate, mussarela, calabresa e cebola',
    imagem_url: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400',
    categoria_id: 1,
    disponivel: true,
    variacoes: [
      { id: 4, tamanho: 'Média', preco: 38.00, disponivel: true },
      { id: 5, tamanho: 'Grande', preco: 48.00, disponivel: true },
    ],
    ingredientes: [],
  };

  const ingredienteExtraMock: Ingrediente = {
    id: 1,
    nome: 'Bacon',
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
            Funcionalidades Implementadas - Sprint 5
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="font-medium text-gray-900 mb-2">✅ Etapa 5.1: Sidebar</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Drawer lateral responsivo</li>
                <li>• Overlay com backdrop</li>
                <li>• Animações slide-in/out</li>
                <li>• Múltiplas formas de fechar</li>
                <li>• Bloqueia scroll do body</li>
                <li>• Estado vazio estilizado</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-2">✅ Etapa 5.2: Items</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Layout compacto e clean</li>
                <li>• Customizações detalhadas</li>
                <li>• Seletor de quantidade inline</li>
                <li>• Botão remover com confirm</li>
                <li>• Preço atualiza em tempo real</li>
                <li>• Badges coloridos (add/remove)</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-2">✅ Etapa 5.3: Resumo</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Contador de produtos/itens</li>
                <li>• Cálculo de subtotal</li>
                <li>• Taxa de entrega (grátis)</li>
                <li>• Total destacado</li>
                <li>• Botão "Finalizar Pedido"</li>
                <li>• Botão "Continuar Comprando"</li>
                <li>• Opção "Limpar carrinho"</li>
              </ul>
            </div>
            <div>
              <h3 className="font-medium text-gray-900 mb-2">✅ Integrações</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• CarrinhoContext completo</li>
                <li>• Persistência em localStorage</li>
                <li>• Cálculos automáticos</li>
                <li>• Callbacks de ações</li>
                <li>• Estados sincronizados</li>
                <li>• TypeScript 100%</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Informações do Resumo */}
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-800 mb-2">
            <strong>Etapa 5.3 - Resumo do Carrinho:</strong>
          </p>
          <ul className="text-sm text-blue-700 space-y-1 list-disc list-inside">
            <li>Contador de produtos únicos vs total de itens</li>
            <li>Subtotal calculado automaticamente pelo Context</li>
            <li>Taxa de entrega exibida (preparada para futuras taxas)</li>
            <li>Total destacado com cores primary</li>
            <li>Ícones nos botões para melhor UX</li>
            <li>Layout visual aprimorado com separadores</li>
          </ul>
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
