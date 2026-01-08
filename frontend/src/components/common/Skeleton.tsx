import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface SkeletonProps {
    /**
     * Variante visual do skeleton
     * @default 'rect'
     */
    variant?: 'text' | 'circle' | 'rect'

    /**
     * Largura do skeleton
     * Pode ser number (px) ou string ('100%', '200px', etc)
     */
    width?: string | number

    /**
     * Altura do skeleton
     * Pode ser number (px) ou string ('100%', '20px', etc)
     */
    height?: string | number

    /**
     * Classes CSS adicionais
     */
    className?: string
}

/**
 * Componente Skeleton para estados de loading
 * 
 * Cria placeholders animados que imitam o conteúdo real
 * enquanto os dados estão sendo carregados.
 * 
 * @example
 * // Texto
 * <Skeleton variant="text" width="60%" height="20px" />
 * 
 * // Círculo (avatar)
 * <Skeleton variant="circle" width="48px" height="48px" />
 * 
 * // Retângulo (imagem)
 * <Skeleton variant="rect" width="100%" height="200px" />
 */
const Skeleton = forwardRef<HTMLDivElement, SkeletonProps>(
    ({ variant = 'rect', width, height, className }, ref) => {
        // Converter width/height para string CSS
        const widthStyle = typeof width === 'number' ? `${width}px` : width
        const heightStyle = typeof height === 'number' ? `${height}px` : height

        return (
            <div
                ref={ref}
                className={cn(
                    // Base styles
                    'bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 bg-[length:200%_100%]',
                    'animate-shimmer',

                    // Variant styles
                    {
                        'rounded': variant === 'rect',
                        'rounded-full': variant === 'circle',
                        'rounded-md': variant === 'text',
                    },

                    // Default dimensions
                    {
                        'h-4': variant === 'text' && !height,
                        'w-24': variant === 'text' && !width,
                    },

                    className
                )}
                style={{
                    width: widthStyle,
                    height: heightStyle,
                }}
                aria-hidden="true"
            />
        )
    }
)

Skeleton.displayName = 'Skeleton'

export default Skeleton
