import { forwardRef } from 'react'
import type { HTMLAttributes } from 'react'
import { Check } from 'lucide-react'
import { cn, formatarPreco } from '@/lib/utils'
import type { ProdutoVariacao } from '@/types/cardapio.types'
import Badge from '@/components/common/Badge'

interface VariacaoSelectorProps extends Omit<HTMLAttributes<HTMLDivElement>, 'onChange'> {
  /**
   * Lista de variações disponíveis
   */
  variacoes: ProdutoVariacao[]

  /**
   * ID da variação selecionada
   */
  variacaoSelecionada?: number

  /**
   * Callback chamado quando uma variação é selecionada
   */
  onChange: (variacao: ProdutoVariacao) => void

  /**
   * Layout do seletor
   * @default 'vertical'
   */
  layout?: 'vertical' | 'horizontal'

  /**
   * Desabilitar seleção
   */
  disabled?: boolean
}

const VariacaoSelector = forwardRef<HTMLDivElement, VariacaoSelectorProps>(
  (
    {
      variacoes,
      variacaoSelecionada,
      onChange,
      layout = 'vertical',
      disabled = false,
      className,
      ...props
    },
    ref
  ) => {
    // Filtrar apenas variações disponíveis
    const variacoesDisponiveis = variacoes.filter((v) => v.disponivel)

    // Se não houver variações disponíveis
    if (variacoesDisponiveis.length === 0) {
      return (
        <div className={cn('p-4 bg-yellow-50 border border-yellow-200 rounded-lg', className)}>
          <p className="text-sm text-yellow-800">
            Nenhuma variação disponível no momento.
          </p>
        </div>
      )
    }

    // Layout classes
    const layoutClasses = {
      vertical: 'flex flex-col gap-2',
      horizontal: 'flex flex-row flex-wrap gap-2',
    }

    return (
      <div
        ref={ref}
        className={cn(layoutClasses[layout], className)}
        role="radiogroup"
        aria-label="Selecione o tamanho"
        {...props}
      >
        {variacoesDisponiveis.map((variacao) => {
          const isSelected = variacaoSelecionada === variacao.id
          const isDisabled = disabled || !variacao.disponivel

          return (
            <button
              key={variacao.id}
              type="button"
              role="radio"
              aria-checked={isSelected}
              disabled={isDisabled}
              onClick={() => !isDisabled && onChange(variacao)}
              className={cn(
                'relative flex items-center justify-between p-4 rounded-lg border-2 transition-all duration-200',
                'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
                // Estados
                isSelected
                  ? 'border-primary-600 bg-primary-50'
                  : 'border-gray-200 bg-white hover:border-primary-300 hover:bg-gray-50',
                isDisabled && 'opacity-50 cursor-not-allowed',
                !isDisabled && 'cursor-pointer',
                // Layout horizontal - largura mínima
                layout === 'horizontal' && 'min-w-[180px]'
              )}
            >
              {/* Conteúdo */}
              <div className="flex-1 text-left">
                <div className="flex items-center gap-2 mb-1">
                  <span
                    className={cn(
                      'font-semibold',
                      isSelected ? 'text-primary-900' : 'text-gray-900'
                    )}
                  >
                    {variacao.tamanho}
                  </span>
                  {!variacao.disponivel && (
                    <Badge variant="error" size="sm">
                      Indisponível
                    </Badge>
                  )}
                </div>
                <p
                  className={cn(
                    'text-lg font-bold',
                    isSelected ? 'text-primary-700' : 'text-gray-700'
                  )}
                >
                  {formatarPreco(variacao.preco)}
                </p>
              </div>

              {/* Indicador de seleção */}
              <div
                className={cn(
                  'flex items-center justify-center w-6 h-6 rounded-full border-2 transition-all duration-200',
                  isSelected
                    ? 'border-primary-600 bg-primary-600'
                    : 'border-gray-300 bg-white'
                )}
              >
                {isSelected && <Check size={16} className="text-white" />}
              </div>
            </button>
          )
        })}
      </div>
    )
  }
)

VariacaoSelector.displayName = 'VariacaoSelector'

export default VariacaoSelector
