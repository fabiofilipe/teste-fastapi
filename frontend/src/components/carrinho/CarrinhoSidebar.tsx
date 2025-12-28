import React, { useEffect } from 'react';
import { createPortal } from 'react-dom';
import { X, ShoppingCart } from 'lucide-react';
import { useCarrinho } from '@/contexts/CarrinhoContext';
import { cn } from '@/lib/utils';
import Button from '@/components/common/Button';
import CarrinhoItem from './CarrinhoItem';

interface CarrinhoSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const CarrinhoSidebar: React.FC<CarrinhoSidebarProps> = ({ isOpen, onClose }) => {
  const { itens, subtotal, totalItens, limparCarrinho, atualizarQuantidade, removerItem } = useCarrinho();

  // Bloquear scroll do body quando sidebar estiver aberto
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  // Fechar ao pressionar ESC
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const formatarPreco = (valor: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(valor);
  };

  const handleFinalizarPedido = () => {
    // TODO: Implementar na próxima etapa
    alert('Funcionalidade de finalizar pedido será implementada em breve!');
  };

  const content = (
    <>
      {/* Overlay/Backdrop */}
      <div
        className={cn(
          'fixed inset-0 bg-black/50 z-40 transition-opacity duration-300',
          isOpen ? 'opacity-100' : 'opacity-0'
        )}
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Sidebar */}
      <div
        className={cn(
          'fixed top-0 right-0 h-full w-full sm:w-96 bg-white shadow-2xl z-50',
          'flex flex-col transition-transform duration-300 ease-in-out',
          isOpen ? 'translate-x-0' : 'translate-x-full'
        )}
        role="dialog"
        aria-modal="true"
        aria-labelledby="carrinho-title"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-primary-50">
          <div className="flex items-center gap-2">
            <ShoppingCart className="w-5 h-5 text-primary-600" />
            <h2 id="carrinho-title" className="text-lg font-semibold text-gray-900">
              Meu Carrinho
            </h2>
            {totalItens > 0 && (
              <span className="px-2 py-0.5 text-xs font-medium bg-primary-600 text-white rounded-full">
                {totalItens}
              </span>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg hover:bg-primary-100 transition-colors"
            aria-label="Fechar carrinho"
          >
            <X className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* Lista de Itens */}
        <div className="flex-1 overflow-y-auto p-4">
          {itens.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center py-12">
              <ShoppingCart className="w-16 h-16 text-gray-300 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Carrinho vazio
              </h3>
              <p className="text-sm text-gray-500 mb-6">
                Adicione produtos ao carrinho para continuar
              </p>
              <Button onClick={onClose} variant="primary">
                Ver Cardápio
              </Button>
            </div>
          ) : (
            <div className="space-y-3">
              {itens.map((item) => (
                <CarrinhoItem
                  key={item.id}
                  item={item}
                  onUpdateQuantidade={atualizarQuantidade}
                  onRemove={removerItem}
                />
              ))}
            </div>
          )}
        </div>

        {/* Footer - Resumo e Ações */}
        {itens.length > 0 && (
          <div className="border-t border-gray-200 bg-gray-50 p-4 space-y-4">
            {/* Resumo de Preços */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Subtotal</span>
                <span className="font-medium text-gray-900">
                  {formatarPreco(subtotal)}
                </span>
              </div>
              <div className="flex justify-between text-lg font-bold border-t border-gray-300 pt-2">
                <span className="text-gray-900">Total</span>
                <span className="text-primary-600">
                  {formatarPreco(subtotal)}
                </span>
              </div>
            </div>

            {/* Botões de Ação */}
            <div className="space-y-2">
              <Button
                onClick={handleFinalizarPedido}
                variant="primary"
                className="w-full"
              >
                Finalizar Pedido
              </Button>
              <Button
                onClick={onClose}
                variant="outline"
                className="w-full"
              >
                Continuar Comprando
              </Button>
            </div>

            {/* Botão Limpar Carrinho */}
            <button
              onClick={() => {
                if (window.confirm('Deseja realmente limpar o carrinho?')) {
                  limparCarrinho();
                }
              }}
              className="w-full text-sm text-red-600 hover:text-red-700 underline transition-colors"
            >
              Limpar carrinho
            </button>
          </div>
        )}
      </div>
    </>
  );

  return createPortal(content, document.body);
};

export default CarrinhoSidebar;
