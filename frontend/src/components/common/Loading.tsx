import { forwardRef } from 'react'
import { cn } from '@/lib/utils'
import { Loader2 } from 'lucide-react'

interface LoadingProps {
  /**
   * Tamanho do indicador de loading
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg'

  /**
   * Texto descritivo opcional
   */
  text?: string

  /**
   * Ocupa a tela inteira com overlay
   */
  fullScreen?: boolean

  /**
   * Variante do indicador
   * @default 'spinner'
   */
  variant?: 'spinner' | 'dots' | 'pulse'

  /**
   * Classes CSS adicionais
   */
  className?: string
}

const Loading = forwardRef<HTMLDivElement, LoadingProps>(
  (
    {
      size = 'md',
      text,
      fullScreen = false,
      variant = 'spinner',
      className,
    },
    ref
  ) => {
    // Tamanhos do spinner
    const spinnerSizes = {
      sm: 16,
      md: 32,
      lg: 64,
    }

    // Tamanhos do texto
    const textSizes = {
      sm: 'text-sm',
      md: 'text-base',
      lg: 'text-lg',
    }

    // Renderizar spinner
    const renderSpinner = () => {
      if (variant === 'spinner') {
        return (
          <Loader2
            className="animate-spin text-blue-600"
            size={spinnerSizes[size]}
          />
        )
      }

      if (variant === 'dots') {
        return (
          <div className="flex gap-1.5">
            {[0, 1, 2].map((i) => (
              <div
                key={i}
                className="rounded-full bg-blue-600 animate-pulse"
                style={{
                  width: size === 'sm' ? 6 : size === 'lg' ? 12 : 8,
                  height: size === 'sm' ? 6 : size === 'lg' ? 12 : 8,
                  animationDelay: `${i * 0.15}s`,
                }}
              />
            ))}
          </div>
        )
      }

      if (variant === 'pulse') {
        return (
          <div
            className="rounded-full bg-blue-600 animate-ping"
            style={{
              width: spinnerSizes[size],
              height: spinnerSizes[size],
            }}
          />
        )
      }

      return null
    }

    const content = (
      <div
        ref={ref}
        className={cn(
          'flex flex-col items-center justify-center gap-3',
          className
        )}
      >
        {renderSpinner()}
        {text && (
          <p className={cn('text-gray-600 font-medium', textSizes[size])}>
            {text}
          </p>
        )}
      </div>
    )

    // Se fullScreen, renderizar com overlay
    if (fullScreen) {
      return (
        <div className="fixed inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center z-50">
          {content}
        </div>
      )
    }

    // Renderizar inline/section
    return content
  }
)

Loading.displayName = 'Loading'

export default Loading
