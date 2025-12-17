import { Pizza, ShoppingCart } from 'lucide-react'
import Badge from '@/components/common/Badge'
import Button from '@/components/common/Button'

interface HeaderProps {
  /**
   * Número de itens no carrinho
   */
  cartItemCount?: number

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
  cartItemCount = 0,
  onCartClick,
  onLogoClick
}: HeaderProps) => {
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
              className="relative"
              aria-label={`Carrinho com ${cartItemCount} ${cartItemCount === 1 ? 'item' : 'itens'}`}
            >
              <ShoppingCart size={24} />
              {cartItemCount > 0 && (
                <span className="absolute -top-1 -right-1">
                  <Badge variant="error" size="sm" className="min-w-[20px] h-5 flex items-center justify-center px-1.5">
                    {cartItemCount > 99 ? '99+' : cartItemCount}
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
