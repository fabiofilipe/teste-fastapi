import { useState, useEffect } from 'react'
import Modal from '@/components/common/Modal'
import Button from '@/components/common/Button'
import Badge from '@/components/common/Badge'
import VariacaoSelector from './VariacaoSelector'
import { formatarPreco } from '@/lib/utils'
import type { Produto, ProdutoVariacao } from '@/types/cardapio.types'
import { ShoppingCart } from 'lucide-react'

interface ProdutoModalProps {
  /**
   * Controla se o modal está aberto
   */
  isOpen: boolean

  /**
   * Callback para fechar o modal
   */
  onClose: () => void

  /**
   * Produto a ser exibido
   */
  produto: Produto | null

  /**
   * Callback ao adicionar ao carrinho
   */
  onAddToCart?: (produto: Produto, variacao: ProdutoVariacao) => void
}

function ProdutoModal({ isOpen, onClose, produto, onAddToCart }: ProdutoModalProps) {
  // Estado da variação selecionada
  const [variacaoSelecionada, setVariacaoSelecionada] = useState<ProdutoVariacao | null>(null)

  // Resetar seleção quando o produto mudar ou modal fechar
  useEffect(() => {
    if (!isOpen || !produto) {
      setVariacaoSelecionada(null)
      return
    }

    // Auto-selecionar primeira variação disponível
    const primeiraVariacao = produto.variacoes.find((v) => v.disponivel)
    if (primeiraVariacao) {
      setVariacaoSelecionada(primeiraVariacao)
    }
  }, [isOpen, produto])

  // Handler para adicionar ao carrinho
  const handleAddToCart = () => {
    if (!produto || !variacaoSelecionada) return

    // TODO: Adicionar lógica completa de customização (Sprint 4.3 e 4.4)
    if (onAddToCart) {
      onAddToCart(produto, variacaoSelecionada)
    }

    // Fechar modal
    onClose()
  }

  // Se não houver produto, não renderizar
  if (!produto) return null

  // URL da imagem (fallback para placeholder)
  const imagemUrl =
    produto.imagem_url ||
    `https://placehold.co/600x400/e2e8f0/64748b?text=${encodeURIComponent(produto.nome)}`

  // Verificar se produto está disponível
  const produtoDisponivel = produto.disponivel && produto.variacoes.some((v) => v.disponivel)

  // Calcular preço base
  const precoBase = variacaoSelecionada?.preco || 0

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="lg"
      className="max-h-[90vh] overflow-hidden flex flex-col"
    >
      {/* Imagem do produto */}
      <div className="relative aspect-[3/2] overflow-hidden bg-gray-100 -mx-6 -mt-4 mb-4">
        <img
          src={imagemUrl}
          alt={produto.nome}
          className="w-full h-full object-cover"
        />
        {!produtoDisponivel && (
          <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
            <Badge variant="error" size="lg">
              Produto Indisponível
            </Badge>
          </div>
        )}
      </div>

      {/* Conteúdo do modal */}
      <div className="space-y-6 flex-1 overflow-y-auto">
        {/* Header do produto */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">{produto.nome}</h2>
          {produto.descricao && (
            <p className="text-gray-600">{produto.descricao}</p>
          )}
        </div>

        {/* Seletor de Variação */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Escolha o tamanho
          </h3>
          <VariacaoSelector
            variacoes={produto.variacoes}
            variacaoSelecionada={variacaoSelecionada?.id}
            onChange={setVariacaoSelecionada}
            disabled={!produtoDisponivel}
          />
        </div>

        {/* Informações sobre ingredientes (placeholder para Sprint 4.3) */}
        {produto.ingredientes.length > 0 && (
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>✨ Customizável:</strong> Este produto possui{' '}
              {produto.ingredientes.length} ingredientes que podem ser personalizados.
              <br />
              <em className="text-xs text-blue-600">
                (Customização de ingredientes será implementada na Etapa 4.3)
              </em>
            </p>
          </div>
        )}

        {/* Resumo de preço (placeholder para Sprint 4.4) */}
        <div className="border-t border-gray-200 pt-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600">Preço base:</span>
            <span className="text-xl font-bold text-primary-600">
              {variacaoSelecionada ? formatarPreco(precoBase) : '—'}
            </span>
          </div>
          <p className="text-xs text-gray-500 italic">
            (Seletor de quantidade e cálculo completo será implementado na Etapa 4.4)
          </p>
        </div>
      </div>

      {/* Footer com ações */}
      <div className="border-t border-gray-200 -mx-6 -mb-4 px-6 py-4 bg-gray-50 flex gap-3">
        <Button
          variant="outline"
          onClick={onClose}
          className="flex-1"
        >
          Cancelar
        </Button>
        <Button
          variant="primary"
          onClick={handleAddToCart}
          disabled={!produtoDisponivel || !variacaoSelecionada}
          leftIcon={<ShoppingCart size={20} />}
          className="flex-1"
        >
          Adicionar ao Carrinho
        </Button>
      </div>
    </Modal>
  )
}

export default ProdutoModal
