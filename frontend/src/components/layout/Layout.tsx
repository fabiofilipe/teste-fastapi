import { cn } from '@/lib/utils'
import Header from './Header'
import Footer from './Footer'

interface LayoutProps {
  /**
   * Conteúdo da página
   */
  children: React.ReactNode

  /**
   * Remove padding do container (útil para hero sections)
   */
  noPadding?: boolean

  /**
   * Largura máxima do container
   * @default '7xl'
   */
  maxWidth?: 'full' | '7xl' | '6xl' | '5xl'

  /**
   * Número de itens no carrinho (passado para o Header)
   */
  cartItemCount?: number

  /**
   * Callback ao clicar no carrinho
   */
  onCartClick?: () => void

  /**
   * Callback ao clicar no logo
   */
  onLogoClick?: () => void
}

const Layout = ({
  children,
  noPadding = false,
  maxWidth = '7xl',
  cartItemCount,
  onCartClick,
  onLogoClick
}: LayoutProps) => {
  const maxWidthClasses = {
    full: 'max-w-full',
    '7xl': 'max-w-7xl',
    '6xl': 'max-w-6xl',
    '5xl': 'max-w-5xl',
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <Header
        cartItemCount={cartItemCount}
        onCartClick={onCartClick}
        onLogoClick={onLogoClick}
      />

      {/* Main Content */}
      <main className="flex-1">
        <div
          className={cn(
            maxWidthClasses[maxWidth],
            'mx-auto',
            !noPadding && 'px-4 md:px-8 py-8'
          )}
        >
          {children}
        </div>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  )
}

export default Layout
