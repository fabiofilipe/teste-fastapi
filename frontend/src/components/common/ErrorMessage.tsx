import { forwardRef } from 'react'
import { cn } from '@/lib/utils'
import { AlertCircle, RefreshCw } from 'lucide-react'
import Button from './Button'

interface ErrorMessageProps {
  /**
   * Título do erro (opcional)
   */
  title?: string

  /**
   * Mensagem de erro
   */
  message: string

  /**
   * Callback ao clicar em "Tentar novamente"
   */
  onRetry?: () => void

  /**
   * Mostra ícone de erro
   * @default true
   */
  showIcon?: boolean

  /**
   * Variante de exibição
   * @default 'card'
   */
  variant?: 'inline' | 'card' | 'fullScreen'

  /**
   * Classes CSS adicionais
   */
  className?: string
}

const ErrorMessage = forwardRef<HTMLDivElement, ErrorMessageProps>(
  (
    {
      title,
      message,
      onRetry,
      showIcon = true,
      variant = 'card',
      className,
    },
    ref
  ) => {
    // Conteúdo do erro
    const errorContent = (
      <>
        {showIcon && (
          <AlertCircle className="text-red-600 flex-shrink-0" size={variant === 'inline' ? 20 : 24} />
        )}
        <div className="flex-1">
          {title && (
            <h3 className="font-semibold text-red-900 mb-1">
              {title}
            </h3>
          )}
          <p className="text-red-800 text-sm">
            {message}
          </p>
        </div>
      </>
    )

    // Renderizar variante inline
    if (variant === 'inline') {
      return (
        <div
          ref={ref}
          className={cn(
            'flex items-center gap-2 text-red-600 animate-in fade-in duration-200',
            className
          )}
        >
          {errorContent}
        </div>
      )
    }

    // Renderizar variante card
    if (variant === 'card') {
      return (
        <div
          ref={ref}
          className={cn(
            'bg-red-50 border border-red-200 rounded-lg p-4 animate-in fade-in duration-200',
            className
          )}
        >
          <div className="flex items-start gap-3">
            {errorContent}
          </div>
          {onRetry && (
            <div className="mt-3 flex justify-end">
              <Button
                variant="outline"
                size="sm"
                onClick={onRetry}
                leftIcon={<RefreshCw size={16} />}
                className="border-red-300 text-red-700 hover:bg-red-100"
              >
                Tentar novamente
              </Button>
            </div>
          )}
        </div>
      )
    }

    // Renderizar variante fullScreen
    if (variant === 'fullScreen') {
      return (
        <div
          ref={ref}
          className={cn(
            'fixed inset-0 bg-white flex items-center justify-center z-50 p-4',
            className
          )}
        >
          <div className="max-w-md w-full text-center space-y-4 animate-in fade-in zoom-in duration-300">
            {showIcon && (
              <div className="flex justify-center">
                <div className="rounded-full bg-red-100 p-4">
                  <AlertCircle className="text-red-600" size={48} />
                </div>
              </div>
            )}
            {title && (
              <h2 className="text-2xl font-bold text-red-900">
                {title}
              </h2>
            )}
            <p className="text-red-800 text-base">
              {message}
            </p>
            {onRetry && (
              <div className="pt-2">
                <Button
                  variant="primary"
                  size="lg"
                  onClick={onRetry}
                  leftIcon={<RefreshCw size={20} />}
                  className="bg-red-600 hover:bg-red-700 focus:ring-red-500"
                >
                  Tentar novamente
                </Button>
              </div>
            )}
          </div>
        </div>
      )
    }

    return null
  }
)

ErrorMessage.displayName = 'ErrorMessage'

export default ErrorMessage
