import { useRef, useEffect, LucideIcon } from 'react';
import { Pizza, Coffee, Wine, IceCream, Dessert, Soup, Salad, Utensils } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Categoria } from '@/types/cardapio.types';

// ============================================================================
// MAPEAMENTO DE ÍCONES POR CATEGORIA
// ============================================================================

const iconMap: Record<string, LucideIcon> = {
  pizza: Pizza,
  pizzas: Pizza,
  bebida: Coffee,
  bebidas: Coffee,
  vinho: Wine,
  vinhos: Wine,
  sobremesa: IceCream,
  sobremesas: IceCream,
  doce: Dessert,
  doces: Dessert,
  sopa: Soup,
  sopas: Soup,
  salada: Salad,
  saladas: Salad,
};

/**
 * Retorna o ícone apropriado baseado no nome da categoria
 */
function getCategoriaIcon(categoriaNome: string): LucideIcon {
  const nomeNormalizado = categoriaNome.toLowerCase().trim();
  return iconMap[nomeNormalizado] || Utensils;
}

// ============================================================================
// PROPS
// ============================================================================

interface CategoriaNavProps {
  /**
   * Lista de categorias a serem exibidas
   */
  categorias: Categoria[];

  /**
   * ID da categoria atualmente selecionada
   */
  categoriaAtiva?: number;

  /**
   * Callback executado ao clicar em uma categoria
   */
  onCategoriaClick: (categoriaId: number) => void;

  /**
   * Classe CSS adicional
   */
  className?: string;
}

// ============================================================================
// COMPONENTE
// ============================================================================

const CategoriaNav = ({
  categorias,
  categoriaAtiva,
  onCategoriaClick,
  className,
}: CategoriaNavProps) => {
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const activeButtonRef = useRef<HTMLButtonElement>(null);

  // ============================================================================
  // AUTO SCROLL TO ACTIVE CATEGORY
  // ============================================================================

  useEffect(() => {
    if (activeButtonRef.current && scrollContainerRef.current) {
      const button = activeButtonRef.current;
      const container = scrollContainerRef.current;

      // Calcula a posição para centralizar o botão ativo
      const buttonLeft = button.offsetLeft;
      const buttonWidth = button.offsetWidth;
      const containerWidth = container.offsetWidth;

      const scrollPosition = buttonLeft - containerWidth / 2 + buttonWidth / 2;

      container.scrollTo({
        left: scrollPosition,
        behavior: 'smooth',
      });
    }
  }, [categoriaAtiva]);

  // ============================================================================
  // RENDER
  // ============================================================================

  // Filtra apenas categorias ativas e ordena pela ordem de exibição
  const categoriasAtivas = categorias
    .filter((cat) => cat.ativa)
    .sort((a, b) => a.ordem_exibicao - b.ordem_exibicao);

  return (
    <nav className={cn('w-full bg-white border-b border-gray-200', className)}>
      <div
        ref={scrollContainerRef}
        className="flex gap-2 px-4 py-3 overflow-x-auto scrollbar-hide scroll-smooth"
        style={{
          scrollbarWidth: 'none',
          msOverflowStyle: 'none',
        }}
      >
        {categoriasAtivas.map((categoria) => {
          const isActive = categoria.id === categoriaAtiva;
          const Icon = getCategoriaIcon(categoria.nome);

          return (
            <button
              key={categoria.id}
              ref={isActive ? activeButtonRef : null}
              onClick={() => onCategoriaClick(categoria.id)}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-full',
                'whitespace-nowrap font-medium text-sm transition-all duration-200',
                'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
                isActive
                  ? 'bg-primary-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200 hover:shadow-sm'
              )}
            >
              <Icon size={18} className={cn(isActive && 'animate-pulse')} />
              <span>{categoria.nome}</span>
              {categoria.produtos && categoria.produtos.length > 0 && (
                <span
                  className={cn(
                    'ml-1 px-2 py-0.5 rounded-full text-xs font-semibold',
                    isActive
                      ? 'bg-primary-700 text-primary-100'
                      : 'bg-gray-200 text-gray-600'
                  )}
                >
                  {categoria.produtos.length}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Gradiente para indicar scroll disponível */}
      <div className="pointer-events-none absolute right-0 top-0 h-full w-8 bg-gradient-to-l from-white to-transparent" />
    </nav>
  );
};

// ============================================================================
// CSS HELPER (adicionar ao index.css)
// ============================================================================

/*
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
*/

export default CategoriaNav;
