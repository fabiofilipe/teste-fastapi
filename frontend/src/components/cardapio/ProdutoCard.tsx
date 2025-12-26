import { forwardRef } from 'react'
import type { HTMLAttributes } from 'react'
import { cn, formatarPreco } from '@/lib/utils'
import type { Produto } from '@/types/cardapio.types'
import Card from '@/components/common/Card'
import Badge from '@/components/common/Badge'
import Button from '@/components/common/Button'

interface ProdutoCardProps extends Omit<HTMLAttributes<HTMLDivElement>, 'onClick'> {
  /**
   * Dados do produto a ser exibido
   */
  produto: Produto

  /**
   * Callback quando o usuário clica em "Ver detalhes"
   */
  onVerDetalhes?: (produto: Produto) => void
}

const ProdutoCard = forwardRef<HTMLDivElement, ProdutoCardProps>(
  ({ produto, onVerDetalhes, className, ...props }, ref) => {
    // Calcular faixa de preços das variações disponíveis
    const variacoesDisponiveis = produto.variacoes.filter((v) => v.disponivel)
    const precos = variacoesDisponiveis.map((v) => v.preco)
    const precoMinimo = precos.length > 0 ? Math.min(...precos) : 0
    const precoMaximo = precos.length > 0 ? Math.max(...precos) : 0

    // Determinar se há variações de preço
    const temVariacaoPreco = precoMinimo !== precoMaximo

    // URL da imagem (fallback para placeholder)
    const imagemUrl =
      produto.imagem_url ||
      `https://placehold.co/400x300/e2e8f0/64748b?text=${encodeURIComponent(produto.nome)}`

    // Handler para ver detalhes
    const handleVerDetalhes = () => {
      if (onVerDetalhes) {
        onVerDetalhes(produto)
      }
    }

    return (
      <Card
        ref={ref}
        variant="interactive"
        padding="none"
        hoverable={produto.disponivel}
        className={cn('overflow-hidden flex flex-col h-full', className)}
        {...props}
      >
        {/* Imagem do produto */}
        <div className="relative aspect-[4/3] overflow-hidden bg-gray-100">
          <img
            src={imagemUrl}
            alt={produto.nome}
            loading="lazy"
            className={cn(
              'w-full h-full object-cover transition-transform duration-300',
              produto.disponivel && 'group-hover:scale-105'
            )}
          />

          {/* Badge de disponibilidade (sobreposto na imagem) */}
          {!produto.disponivel && (
            <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
              <Badge variant="error" size="lg">
                Indisponível
              </Badge>
            </div>
          )}

          {/* Badge de categoria no canto superior direito (opcional) */}
          {produto.disponivel && variacoesDisponiveis.length === 0 && (
            <div className="absolute top-2 right-2">
              <Badge variant="warning" size="sm">
                Sem variações
              </Badge>
            </div>
          )}
        </div>

        {/* Conteúdo do card */}
        <div className="flex flex-col flex-1 p-4">
          {/* Nome e descrição */}
          <div className="flex-1 mb-3">
            <h3 className="font-semibold text-lg text-gray-900 mb-1 line-clamp-2">
              {produto.nome}
            </h3>
            {produto.descricao && (
              <p className="text-sm text-gray-600 line-clamp-2">
                {produto.descricao}
              </p>
            )}
          </div>

          {/* Preço */}
          <div className="mb-3">
            {produto.disponivel && variacoesDisponiveis.length > 0 ? (
              <div className="flex items-baseline gap-1">
                {temVariacaoPreco ? (
                  <>
                    <span className="text-sm text-gray-500">A partir de</span>
                    <span className="text-xl font-bold text-primary-600">
                      {formatarPreco(precoMinimo)}
                    </span>
                    <span className="text-sm text-gray-500">
                      até {formatarPreco(precoMaximo)}
                    </span>
                  </>
                ) : (
                  <span className="text-xl font-bold text-primary-600">
                    {formatarPreco(precoMinimo)}
                  </span>
                )}
              </div>
            ) : (
              <span className="text-sm text-gray-400 italic">
                Consulte disponibilidade
              </span>
            )}
          </div>

          {/* Informações extras */}
          <div className="flex items-center gap-2 mb-3">
            {produto.variacoes.length > 0 && (
              <Badge variant="info" size="sm">
                {produto.variacoes.length}{' '}
                {produto.variacoes.length === 1 ? 'tamanho' : 'tamanhos'}
              </Badge>
            )}
            {produto.ingredientes.length > 0 && (
              <Badge variant="neutral" size="sm">
                Customizável
              </Badge>
            )}
          </div>

          {/* Botão de ação */}
          <Button
            variant={produto.disponivel ? 'primary' : 'outline'}
            size="sm"
            className="w-full"
            onClick={handleVerDetalhes}
            disabled={!produto.disponivel}
          >
            {produto.disponivel ? 'Ver detalhes' : 'Indisponível'}
          </Button>
        </div>
      </Card>
    )
  }
)

ProdutoCard.displayName = 'ProdutoCard'

export default ProdutoCard
