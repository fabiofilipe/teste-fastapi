import { forwardRef } from 'react'
import type { HTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * Variante visual do card
   * @default 'default'
   */
  variant?: 'default' | 'interactive' | 'outlined'

  /**
   * Padding interno do card
   * @default 'md'
   */
  padding?: 'none' | 'sm' | 'md' | 'lg'

  /**
   * Adiciona efeito de hover (elevação e cursor pointer)
   */
  hoverable?: boolean

  children: React.ReactNode
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    {
      variant = 'default',
      padding = 'md',
      hoverable = false,
      className,
      children,
      ...props
    },
    ref
  ) => {
    // Classes base com transições suaves
    const baseStyles = 'rounded-lg transition-all duration-300 ease-out'

    // Variantes
    const variantStyles = {
      default: 'bg-white shadow-sm border border-gray-100',
      interactive: 'bg-white shadow-sm border border-gray-100',
      outlined: 'bg-white border-2 border-gray-200',
    }

    // Efeito de hover com feedback visual aprimorado
    const hoverStyles = hoverable
      ? variant === 'interactive'
        ? 'hover:shadow-lg hover:-translate-y-1 hover:scale-[1.01] cursor-pointer active:scale-[0.99] active:translate-y-0'
        : 'hover:shadow-md hover:scale-[1.01] cursor-pointer active:scale-[0.99]'
      : ''

    // Padding
    const paddingStyles = {
      none: 'p-0',
      sm: 'p-3',
      md: 'p-4',
      lg: 'p-6',
    }

    return (
      <div
        ref={ref}
        className={cn(
          baseStyles,
          variantStyles[variant],
          paddingStyles[padding],
          hoverStyles,
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)

Card.displayName = 'Card'

export default Card
