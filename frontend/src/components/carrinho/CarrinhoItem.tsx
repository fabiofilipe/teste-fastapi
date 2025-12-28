import React from 'react';
import { Trash2, Plus, Minus } from 'lucide-react';
import type { ItemCarrinho } from '@/contexts/CarrinhoContext';
import { cn } from '@/lib/utils';

interface CarrinhoItemProps {
  item: ItemCarrinho;
  onUpdateQuantidade: (id: string, quantidade: number) => void;
  onRemove: (id: string) => void;
}

const CarrinhoItem: React.FC<CarrinhoItemProps> = ({
  item,
  onUpdateQuantidade,
  onRemove,
}) => {
  const formatarPreco = (valor: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(valor);
  };

  const precoUnitario = item.preco_total / item.quantidade;

  const handleIncrement = () => {
    if (item.quantidade < 10) {
      onUpdateQuantidade(item.id, item.quantidade + 1);
    }
  };

  const handleDecrement = () => {
    if (item.quantidade > 1) {
      onUpdateQuantidade(item.id, item.quantidade - 1);
    }
  };

  const handleRemove = () => {
    if (window.confirm(`Remover ${item.produto.nome} do carrinho?`)) {
      onRemove(item.id);
    }
  };

  return (
    <div className="p-4 border border-gray-200 rounded-lg bg-white hover:shadow-md transition-shadow">
      {/* Header: Nome + Botão Remover */}
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 leading-tight">
            {item.produto.nome}
          </h3>
          <p className="text-sm text-gray-600 mt-0.5">
            {item.variacao.tamanho}
          </p>
        </div>
        <button
          onClick={handleRemove}
          className="p-1.5 rounded-lg hover:bg-red-50 text-red-600 hover:text-red-700 transition-colors"
          aria-label="Remover item"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>

      {/* Customizações */}
      {(item.ingredientesAdicionados.length > 0 ||
        item.ingredientesRemovidos.length > 0 ||
        item.observacoes) && (
        <div className="mb-3 pb-3 border-b border-gray-100">
          {/* Ingredientes Adicionados */}
          {item.ingredientesAdicionados.length > 0 && (
            <div className="mb-1">
              <p className="text-xs text-green-700 font-medium mb-0.5">
                Adicionados:
              </p>
              <div className="flex flex-wrap gap-1">
                {item.ingredientesAdicionados.map((ing) => (
                  <span
                    key={ing.id}
                    className="inline-flex items-center gap-1 px-2 py-0.5 bg-green-50 text-green-700 text-xs rounded-full"
                  >
                    <Plus className="w-3 h-3" />
                    {ing.nome}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Ingredientes Removidos */}
          {item.ingredientesRemovidos.length > 0 && (
            <div className="mb-1">
              <p className="text-xs text-red-700 font-medium mb-0.5">
                Removidos:
              </p>
              <div className="flex flex-wrap gap-1">
                {item.ingredientesRemovidos.map((id) => (
                  <span
                    key={id}
                    className="inline-flex items-center gap-1 px-2 py-0.5 bg-red-50 text-red-700 text-xs rounded-full"
                  >
                    <Minus className="w-3 h-3" />
                    ID {id}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Observações */}
          {item.observacoes && (
            <div className="mt-2">
              <p className="text-xs text-gray-600 italic">
                "{item.observacoes}"
              </p>
            </div>
          )}
        </div>
      )}

      {/* Footer: Quantidade + Preço */}
      <div className="flex items-center justify-between gap-4">
        {/* Seletor de Quantidade */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleDecrement}
            disabled={item.quantidade <= 1}
            className={cn(
              'w-7 h-7 rounded-lg border flex items-center justify-center transition-all',
              item.quantidade <= 1
                ? 'border-gray-200 text-gray-300 cursor-not-allowed'
                : 'border-primary-600 text-primary-600 hover:bg-primary-50 active:scale-95'
            )}
            aria-label="Diminuir quantidade"
          >
            <Minus className="w-3.5 h-3.5" />
          </button>

          <span className="w-8 text-center font-medium text-gray-900">
            {item.quantidade}
          </span>

          <button
            onClick={handleIncrement}
            disabled={item.quantidade >= 10}
            className={cn(
              'w-7 h-7 rounded-lg border flex items-center justify-center transition-all',
              item.quantidade >= 10
                ? 'border-gray-200 text-gray-300 cursor-not-allowed'
                : 'border-primary-600 bg-primary-600 text-white hover:bg-primary-700 active:scale-95'
            )}
            aria-label="Aumentar quantidade"
          >
            <Plus className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Preços */}
        <div className="text-right">
          {item.quantidade > 1 && (
            <p className="text-xs text-gray-500 line-through">
              {formatarPreco(precoUnitario)} × {item.quantidade}
            </p>
          )}
          <p className="text-base font-bold text-primary-600">
            {formatarPreco(item.preco_total)}
          </p>
        </div>
      </div>
    </div>
  );
};

export default CarrinhoItem;
