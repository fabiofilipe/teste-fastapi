import { forwardRef } from 'react'
import type { HTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  /**
   * Variante de cor do badge
   * @default 'neutral'
   */
  variant?: 'success' | 'warning' | 'error' | 'info' | 'neutral'

  /**
   * Tamanho do badge
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg'

  /**
   * Mostra um ponto colorido antes do texto
   */
  dot?: boolean

  children: React.ReactNode
}

const Badge = forwardRef<HTMLSpanElement, BadgeProps>(
  (
    {
      variant = 'neutral',
      size = 'md',
      dot = false,
      className,
      children,
      ...props
    },
    ref
  ) => {
    // Classes base
    const baseStyles = 'inline-flex items-center gap-1.5 font-medium rounded-full transition-colors'

    // Variantes de cor
    const variantStyles = {
      success: 'bg-green-100 text-green-800 border border-green-200',
      warning: 'bg-yellow-100 text-yellow-800 border border-yellow-200',
      error: 'bg-red-100 text-red-800 border border-red-200',
      info: 'bg-blue-100 text-blue-800 border border-blue-200',
      neutral: 'bg-gray-100 text-gray-800 border border-gray-200',
    }

    // Cor do dot
    const dotStyles = {
      success: 'bg-green-500',
      warning: 'bg-yellow-500',
      error: 'bg-red-500',
      info: 'bg-blue-500',
      neutral: 'bg-gray-500',
    }

    // Tamanhos
    const sizeStyles = {
      sm: 'text-xs px-2 py-0.5',
      md: 'text-sm px-2.5 py-1',
      lg: 'text-base px-3 py-1.5',
    }

    // Tamanho do dot
    const dotSizeStyles = {
      sm: 'w-1.5 h-1.5',
      md: 'w-2 h-2',
      lg: 'w-2.5 h-2.5',
    }

    return (
      <span
        ref={ref}
        className={cn(
          baseStyles,
          variantStyles[variant],
          sizeStyles[size],
          className
        )}
        {...props}
      >
        {dot && (
          <span
            className={cn(
              'rounded-full',
              dotStyles[variant],
              dotSizeStyles[size]
            )}
          />
        )}
        {children}
      </span>
    )
  }
)

Badge.displayName = 'Badge'

export default Badge
