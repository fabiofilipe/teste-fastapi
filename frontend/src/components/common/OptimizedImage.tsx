import { useState, useEffect, useRef } from 'react'
import type { ImgHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

interface OptimizedImageProps extends Omit<ImgHTMLAttributes<HTMLImageElement>, 'placeholder'> {
  /**
   * URL da imagem
   */
  src: string

  /**
   * Texto alternativo
   */
  alt: string

  /**
   * Ativa blur placeholder durante carregamento
   * @default true
   */
  useBlur?: boolean

  /**
   * Classes CSS adicionais
   */
  className?: string

  /**
   * Callback quando a imagem carregar
   */
  onLoad?: () => void

  /**
   * Callback quando houver erro
   */
  onError?: () => void
}

function OptimizedImage({
  src,
  alt,
  useBlur = true,
  className,
  onLoad,
  onError,
  ...props
}: OptimizedImageProps) {
  const [isLoading, setIsLoading] = useState(true)
  const [hasError, setHasError] = useState(false)
  const imgRef = useRef<HTMLImageElement>(null)

  // Resetar estado quando src mudar
  useEffect(() => {
    setIsLoading(true)
    setHasError(false)
  }, [src])

  // Handler de carregamento
  const handleLoad = () => {
    setIsLoading(false)
    onLoad?.()
  }

  // Handler de erro
  const handleError = () => {
    setIsLoading(false)
    setHasError(true)
    onError?.()
  }

  // Se houver erro, mostrar placeholder
  if (hasError) {
    return (
      <div
        className={cn(
          'flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200',
          className
        )}
      >
        <svg
          className="w-12 h-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
        </svg>
      </div>
    )
  }

  return (
    <div className="relative overflow-hidden">
      {/* Blur placeholder */}
      {useBlur && isLoading && (
        <div
          className={cn(
            'absolute inset-0 bg-gradient-to-br from-gray-200 to-gray-300 animate-pulse',
            className
          )}
        />
      )}

      {/* Imagem */}
      <img
        ref={imgRef}
        src={src}
        alt={alt}
        loading="lazy"
        onLoad={handleLoad}
        onError={handleError}
        className={cn(
          'transition-opacity duration-500',
          isLoading ? 'opacity-0' : 'opacity-100',
          className
        )}
        {...props}
      />
    </div>
  )
}

export default OptimizedImage
