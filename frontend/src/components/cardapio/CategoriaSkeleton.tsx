import { forwardRef } from 'react'
import Skeleton from '@/components/common/Skeleton'
import { cn } from '@/lib/utils'

interface CategoriaSkeletonProps {
    /**
     * Número de categorias skeleton a exibir
     * @default 6
     */
    count?: number

    /**
     * Classes CSS adicionais
     */
    className?: string
}

/**
 * Skeleton para o componente CategoriaNav
 * 
 * Replica a estrutura visual da navegação de categorias durante o loading.
 * Mostra múltiplas tabs horizontais com ícone e texto.
 */
const CategoriaSkeleton = forwardRef<HTMLDivElement, CategoriaSkeletonProps>(
    ({ count = 6, className }, ref) => {
        return (
            <div
                ref={ref}
                className={cn(
                    'flex gap-3 overflow-x-auto scrollbar-hide py-1',
                    className
                )}
                aria-hidden="true"
            >
                {Array.from({ length: count }).map((_, index) => (
                    <div
                        key={index}
                        className="flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-200 bg-white flex-shrink-0"
                    >
                        {/* Ícone (círculo) */}
                        <Skeleton
                            variant="circle"
                            width="24px"
                            height="24px"
                        />

                        {/* Nome da categoria */}
                        <Skeleton
                            variant="text"
                            width="80px"
                            height="14px"
                        />

                        {/* Badge de contagem */}
                        <Skeleton
                            variant="text"
                            width="24px"
                            height="18px"
                            className="rounded-full"
                        />
                    </div>
                ))}
            </div>
        )
    }
)

CategoriaSkeleton.displayName = 'CategoriaSkeleton'

export default CategoriaSkeleton
