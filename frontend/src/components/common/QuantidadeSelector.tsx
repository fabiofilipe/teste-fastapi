import { forwardRef } from 'react'
import type { HTMLAttributes } from 'react'
import { cn } from '@/lib/utils'
import { Plus, Minus } from 'lucide-react'

interface QuantidadeSelectorProps extends Omit<HTMLAttributes<HTMLDivElement>, 'onChange'> {
  /**
   * Quantidade atual
   */
  quantidade: number

  /**
   * Callback quando a quantidade muda
   */
  onChange: (quantidade: number) => void

  /**
   * Quantidade mínima permitida
   * @default 1
   */
  min?: number

  /**
   * Quantidade máxima permitida
   * @default 10
   */
  max?: number

  /**
   * Desabilitar seletor
   */
  disabled?: boolean

  /**
   * Tamanho do seletor
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg'
}

const QuantidadeSelector = forwardRef<HTMLDivElement, QuantidadeSelectorProps>(
  (
    {
      quantidade,
      onChange,
      min = 1,
      max = 10,
      disabled = false,
      size = 'md',
      className,
      ...props
    },
    ref
  ) => {
    // Handler para incrementar
    const handleIncrement = () => {
      if (quantidade < max && !disabled) {
        onChange(quantidade + 1)
      }
    }

    // Handler para decrementar
    const handleDecrement = () => {
      if (quantidade > min && !disabled) {
        onChange(quantidade - 1)
      }
    }

    // Verificar limites
    const isMinDisabled = quantidade <= min || disabled
    const isMaxDisabled = quantidade >= max || disabled

    // Tamanhos
    const sizeStyles = {
      sm: {
        container: 'h-8',
        button: 'w-8 h-8',
        icon: 14,
        text: 'text-sm',
      },
      md: {
        container: 'h-10',
        button: 'w-10 h-10',
        icon: 16,
        text: 'text-base',
      },
      lg: {
        container: 'h-12',
        button: 'w-12 h-12',
        icon: 20,
        text: 'text-lg',
      },
    }

    const currentSize = sizeStyles[size]

    return (
      <div
        ref={ref}
        className={cn('inline-flex items-center gap-2', className)}
        role="group"
        aria-label="Seletor de quantidade"
        {...props}
      >
        {/* Botão Diminuir */}
        <button
          type="button"
          onClick={handleDecrement}
          disabled={isMinDisabled}
          aria-label="Diminuir quantidade"
          className={cn(
            currentSize.button,
            'flex items-center justify-center rounded-lg border-2 transition-all',
            'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-1',
            isMinDisabled
              ? 'border-gray-200 bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'border-primary-600 bg-white text-primary-600 hover:bg-primary-50 active:bg-primary-100'
          )}
        >
          <Minus size={currentSize.icon} />
        </button>

        {/* Display da Quantidade */}
        <div
          className={cn(
            'flex items-center justify-center min-w-[3rem] px-3 font-bold text-gray-900',
            currentSize.container,
            currentSize.text,
            disabled && 'opacity-50'
          )}
          aria-live="polite"
          aria-atomic="true"
        >
          {quantidade}
        </div>

        {/* Botão Aumentar */}
        <button
          type="button"
          onClick={handleIncrement}
          disabled={isMaxDisabled}
          aria-label="Aumentar quantidade"
          className={cn(
            currentSize.button,
            'flex items-center justify-center rounded-lg border-2 transition-all',
            'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-1',
            isMaxDisabled
              ? 'border-gray-200 bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'border-primary-600 bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800'
          )}
        >
          <Plus size={currentSize.icon} />
        </button>
      </div>
    )
  }
)

QuantidadeSelector.displayName = 'QuantidadeSelector'

export default QuantidadeSelector
