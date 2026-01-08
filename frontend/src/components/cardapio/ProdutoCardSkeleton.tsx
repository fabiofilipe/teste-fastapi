import { forwardRef } from 'react'
import Skeleton from '@/components/common/Skeleton'
import { cn } from '@/lib/utils'

interface ProdutoCardSkeletonProps {
    /**
     * Classes CSS adicionais
     */
    className?: string
}

/**
 * Skeleton para o componente ProdutoCard
 * 
 * Replica a estrutura visual do card de produto durante o loading.
 * Usado no grid de produtos enquanto os dados são carregados da API.
 */
const ProdutoCardSkeleton = forwardRef<HTMLDivElement, ProdutoCardSkeletonProps>(
    ({ className }, ref) => {
        return (
            <div
                ref={ref}
                className={cn(
                    'bg-white rounded-lg border border-gray-200 overflow-hidden',
                    className
                )}
                aria-hidden="true"
            >
                {/* Imagem */}
                <Skeleton
                    variant="rect"
                    className="w-full aspect-[4/3]"
                />

                {/* Conteúdo */}
                <div className="p-4 space-y-3">
                    {/* Nome do produto (2 linhas) */}
                    <div className="space-y-2">
                        <Skeleton variant="text" width="85%" height="16px" />
                        <Skeleton variant="text" width="65%" height="16px" />
                    </div>

                    {/* Descrição (1 linha) */}
                    <Skeleton variant="text" width="100%" height="14px" />

                    {/* Badges e preço */}
                    <div className="flex items-center justify-between pt-2">
                        <Skeleton variant="text" width="60px" height="20px" className="rounded-full" />
                        <Skeleton variant="text" width="80px" height="18px" />
                    </div>

                    {/* Botão */}
                    <Skeleton variant="rect" width="100%" height="36px" />
                </div>
            </div>
        )
    }
)

ProdutoCardSkeleton.displayName = 'ProdutoCardSkeleton'

export default ProdutoCardSkeleton
