import { Pizza, ShoppingCart } from 'lucide-react'
import { useCarrinho } from '@/contexts/CarrinhoContext'
import Badge from '@/components/common/Badge'
import Button from '@/components/common/Button'
import Tooltip from '@/components/common/Tooltip'

interface HeaderProps {
  /**
   * Callback ao clicar no carrinho
   */
  onCartClick?: () => void

  /**
   * Callback ao clicar no logo (volta para home)
   */
  onLogoClick?: () => void
}

const Header = ({
  onCartClick,
  onLogoClick
}: HeaderProps) => {
  const { totalItens } = useCarrinho();
  return (
    <header className="sticky top-0 z-50 bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 md:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo e Nome */}
          <button
            onClick={onLogoClick}
            className="flex items-center gap-2 hover:opacity-80 transition-opacity focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-lg px-2 py-1"
            aria-label="Voltar para início"
          >
            <Pizza className="text-red-600" size={32} />
            <div className="flex flex-col items-start">
              <span className="text-xl font-bold text-gray-900">
                Pizzaria
              </span>
              <span className="text-xs text-gray-500 hidden sm:block">
                Sabor em cada fatia
              </span>
            </div>
          </button>

          {/* Carrinho */}
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="md"
              onClick={onCartClick}
              className="relative group"
              aria-label={`Carrinho com ${totalItens} ${totalItens === 1 ? 'item' : 'itens'}`}
            >
              <ShoppingCart
                size={24}
                className={totalItens > 0 ? 'text-primary-600 group-hover:scale-110 transition-transform' : 'group-hover:scale-110 transition-transform'}
              />
              {totalItens > 0 && (
                <span className="absolute -top-1 -right-1 animate-in zoom-in-50 duration-200">
                  <Badge
                    variant="error"
                    size="sm"
                    className="min-w-[20px] h-5 flex items-center justify-center px-1.5 font-bold shadow-md animate-pulse"
                  >
                    {totalItens > 99 ? '99+' : totalItens}
                  </Badge>
                </span>
              )}
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
