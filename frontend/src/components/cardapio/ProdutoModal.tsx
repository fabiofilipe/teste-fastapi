import { useState, useEffect } from 'react'
import Modal from '@/components/common/Modal'
import Button from '@/components/common/Button'
import Badge from '@/components/common/Badge'
import QuantidadeSelector from '@/components/common/QuantidadeSelector'
import OptimizedImage from '@/components/common/OptimizedImage'
import VariacaoSelector from './VariacaoSelector'
import IngredientesCustomizacao from './IngredientesCustomizacao'
import { formatarPreco } from '@/lib/utils'
import type { Produto, ProdutoVariacao, Ingrediente } from '@/types/cardapio.types'
import { ShoppingCart } from 'lucide-react'

interface CustomizacaoData {
  ingredientesAdicionados: Ingrediente[]
  ingredientesRemovidos: number[]
  observacoes: string
  precoIngredientes: number
}

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
  onAddToCart?: (
    produto: Produto,
    variacao: ProdutoVariacao,
    customizacao: CustomizacaoData,
    quantidade: number
  ) => void
}

function ProdutoModal({ isOpen, onClose, produto, onAddToCart }: ProdutoModalProps) {
  // Estado da variação selecionada
  const [variacaoSelecionada, setVariacaoSelecionada] = useState<ProdutoVariacao | null>(null)

  // Estado da customização de ingredientes
  const [customizacao, setCustomizacao] = useState<CustomizacaoData>({
    ingredientesAdicionados: [],
    ingredientesRemovidos: [],
    observacoes: '',
    precoIngredientes: 0,
  })

  // Estado da quantidade
  const [quantidade, setQuantidade] = useState(1)

  // Resetar seleção quando o produto mudar ou modal fechar
  useEffect(() => {
    if (!isOpen || !produto) {
      setVariacaoSelecionada(null)
      setCustomizacao({
        ingredientesAdicionados: [],
        ingredientesRemovidos: [],
        observacoes: '',
        precoIngredientes: 0,
      })
      setQuantidade(1)
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

    if (onAddToCart) {
      onAddToCart(produto, variacaoSelecionada, customizacao, quantidade)
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

  // Calcular preços
  const precoBase = variacaoSelecionada?.preco || 0
  const precoUnitario = precoBase + customizacao.precoIngredientes
  const precoTotal = precoUnitario * quantidade

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="lg"
      className="max-h-[90vh] sm:max-h-[85vh] overflow-hidden flex flex-col"
      contentClassName="p-0"
    >
      {/* Imagem do produto */}
      <div className="relative aspect-[4/3] sm:aspect-[3/2] overflow-hidden bg-gray-100">
        <OptimizedImage
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
      <div className="space-y-4 sm:space-y-6 flex-1 overflow-y-auto px-4 sm:px-6 py-4">
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

        {/* Customização de Ingredientes */}
        {produto.ingredientes.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Personalize seu produto
            </h3>
            <IngredientesCustomizacao
              produto={produto}
              onChange={setCustomizacao}
            />
          </div>
        )}

        {/* Quantidade */}
        <div>
          <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-3">
            Quantidade
          </h3>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200 gap-3 sm:gap-0">
            <span className="text-sm text-gray-700">
              Quantas unidades você deseja?
            </span>
            <QuantidadeSelector
              quantidade={quantidade}
              onChange={setQuantidade}
              min={1}
              max={10}
              disabled={!produtoDisponivel}
            />
          </div>
        </div>

        {/* Resumo de preço */}
        <div className="border-t border-gray-200 pt-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Resumo do Pedido
          </h3>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Preço base:</span>
              <span className="text-base font-semibold text-gray-900">
                {variacaoSelecionada ? formatarPreco(precoBase) : '—'}
              </span>
            </div>
            {customizacao.precoIngredientes > 0 && (
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Ingredientes adicionais:</span>
                <span className="text-base font-semibold text-green-600">
                  + {formatarPreco(customizacao.precoIngredientes)}
                </span>
              </div>
            )}
            {quantidade > 1 && (
              <>
                <div className="flex items-center justify-between pt-2 border-t border-gray-200">
                  <span className="text-sm text-gray-600">Subtotal unitário:</span>
                  <span className="text-base font-semibold text-gray-900">
                    {formatarPreco(precoUnitario)}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Quantidade:</span>
                  <span className="text-base font-semibold text-gray-900">
                    × {quantidade}
                  </span>
                </div>
              </>
            )}
            <div className="flex items-center justify-between pt-3 border-t-2 border-gray-300">
              <span className="text-lg font-bold text-gray-900">Total:</span>
              <span className="text-2xl font-bold text-primary-600">
                {variacaoSelecionada ? formatarPreco(precoTotal) : '—'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer com ações */}
      <div className="border-t border-gray-200 px-4 sm:px-6 py-4 bg-gray-50 flex flex-col sm:flex-row gap-3">
        <Button
          variant="outline"
          onClick={onClose}
          className="flex-1 w-full sm:w-auto order-2 sm:order-1"
        >
          Cancelar
        </Button>
        <Button
          variant="primary"
          onClick={handleAddToCart}
          disabled={!produtoDisponivel || !variacaoSelecionada}
          leftIcon={<ShoppingCart size={20} />}
          className="flex-1 w-full sm:w-auto order-1 sm:order-2"
        >
          Adicionar ao Carrinho
        </Button>
      </div>
    </Modal>
  )
}

export default ProdutoModal
