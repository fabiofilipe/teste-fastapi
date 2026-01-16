import { forwardRef } from 'react'
import type { ButtonHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'
import { Loader2 } from 'lucide-react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * Variante visual do botão
   * @default 'primary'
   */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'

  /**
   * Tamanho do botão
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg'

  /**
   * Mostra spinner de loading e desabilita o botão
   */
  isLoading?: boolean

  /**
   * Ícone à esquerda do texto
   */
  leftIcon?: React.ReactNode

  /**
   * Ícone à direita do texto
   */
  rightIcon?: React.ReactNode

  children: React.ReactNode
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      leftIcon,
      rightIcon,
      className,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    // Classes base com melhor feedback visual e focus visible
    const baseStyles = 'inline-flex items-center justify-center gap-2 font-medium rounded-lg transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed hover:scale-[1.02] active:scale-[0.98]'

    // Variantes de estilo com focus visible de alto contraste
    const variantStyles = {
      primary: 'bg-primary-600 text-white hover:bg-primary-700 hover:shadow-md focus-visible:ring-primary-600 active:bg-primary-800',
      secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 hover:shadow-sm focus-visible:ring-gray-500 active:bg-gray-400',
      outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 hover:shadow-sm focus-visible:ring-primary-600 active:bg-primary-100 active:border-primary-700',
      ghost: 'text-gray-700 hover:bg-gray-100 focus-visible:ring-gray-500 active:bg-gray-200',
      danger: 'bg-red-600 text-white hover:bg-red-700 hover:shadow-md focus-visible:ring-red-600 active:bg-red-800',
    }

    // Tamanhos
    const sizeStyles = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg',
    }

    return (
      <button
        ref={ref}
        className={cn(
          baseStyles,
          variantStyles[variant],
          sizeStyles[size],
          className
        )}
        disabled={disabled || isLoading}
        aria-busy={isLoading}
        {...props}
      >
        {isLoading && (
          <Loader2 className="animate-spin" size={size === 'sm' ? 14 : size === 'lg' ? 20 : 16} aria-hidden="true" />
        )}

        {!isLoading && leftIcon && leftIcon}

        {children}

        {!isLoading && rightIcon && rightIcon}
      </button>
    )
  }
)

Button.displayName = 'Button'

export default Button
