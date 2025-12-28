import { useState } from 'react'
import { cn } from '@/lib/utils'
import Header from './Header'
import Footer from './Footer'
import CarrinhoSidebar from '@/components/carrinho/CarrinhoSidebar'

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
   * Callback ao clicar no logo
   */
  onLogoClick?: () => void
}

const Layout = ({
  children,
  noPadding = false,
  maxWidth = '7xl',
  onLogoClick
}: LayoutProps) => {
  const [isCarrinhoOpen, setIsCarrinhoOpen] = useState(false);
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
        onCartClick={() => setIsCarrinhoOpen(true)}
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

      {/* Carrinho Sidebar */}
      <CarrinhoSidebar
        isOpen={isCarrinhoOpen}
        onClose={() => setIsCarrinhoOpen(false)}
      />
    </div>
  )
}

export default Layout
