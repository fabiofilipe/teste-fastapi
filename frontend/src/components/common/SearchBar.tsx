import { useState, useEffect, useRef, forwardRef } from 'react'
import { Search, X, Loader2 } from 'lucide-react'
import { useBuscaProdutos } from '@/hooks/useCardapio'
import type { Produto } from '@/types/cardapio.types'
import { cn } from '@/lib/utils'

interface SearchBarProps {
    /**
     * Callback ao selecionar um produto nos resultados
     */
    onSelectProduct?: (produto: Produto) => void

    /**
     * Callback ao fechar/limpar a busca
     */
    onClose?: () => void

    /**
     * Placeholder do input
     */
    placeholder?: string

    /**
     * Classes CSS adicionais
     */
    className?: string

    /**
     * Foco automático ao montar
     */
    autoFocus?: boolean
}

const SearchBar = forwardRef<HTMLInputElement, SearchBarProps>(
    (
        {
            onSelectProduct,
            onClose,
            placeholder = 'Buscar produtos...',
            className,
            autoFocus = false,
        },
        ref
    ) => {
        const [inputValue, setInputValue] = useState('')
        const [debouncedValue, setDebouncedValue] = useState('')
        const [isOpen, setIsOpen] = useState(false)
        const [selectedIndex, setSelectedIndex] = useState(-1)

        const dropdownRef = useRef<HTMLDivElement>(null)
        const inputRef = useRef<HTMLInputElement>(null)

        // Combina refs (externa e interna)
        useEffect(() => {
            if (ref && inputRef.current) {
                if (typeof ref === 'function') {
                    ref(inputRef.current)
                } else {
                    ref.current = inputRef.current
                }
            }
        }, [ref])

        // Debounce do termo de busca (300ms)
        useEffect(() => {
            const timer = setTimeout(() => {
                setDebouncedValue(inputValue)
            }, 300)

            return () => clearTimeout(timer)
        }, [inputValue])

        // Query de busca (só ativa com 2+ caracteres)
        const { data: produtos, isLoading } = useBuscaProdutos(debouncedValue)

        // Abre dropdown quando há resultados
        useEffect(() => {
            if (debouncedValue.length >= 2 && produtos) {
                setIsOpen(true)
                setSelectedIndex(-1)
            } else {
                setIsOpen(false)
            }
        }, [produtos, debouncedValue])

        // Fecha dropdown ao clicar fora
        useEffect(() => {
            const handleClickOutside = (event: MouseEvent) => {
                if (
                    dropdownRef.current &&
                    !dropdownRef.current.contains(event.target as Node) &&
                    inputRef.current &&
                    !inputRef.current.contains(event.target as Node)
                ) {
                    setIsOpen(false)
                }
            }

            document.addEventListener('mousedown', handleClickOutside)
            return () => document.removeEventListener('mousedown', handleClickOutside)
        }, [])

        // Navegação por teclado
        const handleKeyDown = (e: React.KeyboardEvent) => {
            if (!produtos || produtos.length === 0) return

            switch (e.key) {
                case 'ArrowDown':
                    e.preventDefault()
                    setSelectedIndex((prev) =>
                        prev < produtos.length - 1 ? prev + 1 : prev
                    )
                    break

                case 'ArrowUp':
                    e.preventDefault()
                    setSelectedIndex((prev) => (prev > 0 ? prev - 1 : -1))
                    break

                case 'Enter':
                    e.preventDefault()
                    if (selectedIndex >= 0 && produtos[selectedIndex]) {
                        handleSelectProduct(produtos[selectedIndex])
                    }
                    break

                case 'Escape':
                    e.preventDefault()
                    handleClear()
                    break
            }
        }

        // Selecionar produto
        const handleSelectProduct = (produto: Produto) => {
            onSelectProduct?.(produto)
            handleClear()
            setIsOpen(false)
        }

        // Limpar busca
        const handleClear = () => {
            setInputValue('')
            setDebouncedValue('')
            setIsOpen(false)
            setSelectedIndex(-1)
            onClose?.()
            inputRef.current?.focus()
        }

        // Destaque do termo buscado
        const highlightTerm = (text: string, term: string) => {
            if (!term) return text

            const regex = new RegExp(`(${term})`, 'gi')
            const parts = text.split(regex)

            return (
                <>
                    {parts.map((part, index) =>
                        regex.test(part) ? (
                            <mark
                                key={index}
                                className="bg-yellow-200 text-gray-900 font-semibold"
                            >
                                {part}
                            </mark>
                        ) : (
                            part
                        )
                    )}
                </>
            )
        }

        // Formatação de preço
        const formatarPreco = (preco: number) => {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL',
            }).format(preco)
        }

        // Faixa de preços do produto
        const getFaixaPrecos = (produto: Produto) => {
            const variacoesDisponiveis = produto.variacoes.filter((v) => v.disponivel)

            if (variacoesDisponiveis.length === 0) {
                return 'Indisponível'
            }

            const precos = variacoesDisponiveis.map((v) => v.preco)
            const minPreco = Math.min(...precos)
            const maxPreco = Math.max(...precos)

            if (minPreco === maxPreco) {
                return formatarPreco(minPreco)
            }

            return `${formatarPreco(minPreco)} - ${formatarPreco(maxPreco)}`
        }

        return (
            <div className={cn('relative w-full', className)}>
                {/* Input de busca */}
                <div className="relative">
                    <div className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none">
                        <Search className="w-5 h-5 text-gray-400" />
                    </div>

                    <input
                        ref={inputRef}
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder={placeholder}
                        autoFocus={autoFocus}
                        className={cn(
                            'w-full pl-10 pr-10 py-2.5 border border-gray-300 rounded-lg',
                            'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                            'placeholder:text-gray-400',
                            'transition-all duration-200'
                        )}
                        aria-label="Buscar produtos"
                        aria-autocomplete="list"
                        aria-controls="search-results"
                        aria-expanded={isOpen}
                    />

                    {/* Indicador de loading ou botão limpar */}
                    <div className="absolute right-3 top-1/2 -translate-y-1/2">
                        {isLoading && debouncedValue.length >= 2 ? (
                            <Loader2 className="w-5 h-5 text-gray-400 animate-spin" />
                        ) : inputValue.length > 0 ? (
                            <button
                                onClick={handleClear}
                                className="p-1 hover:bg-gray-100 rounded-full transition-colors"
                                aria-label="Limpar busca"
                            >
                                <X className="w-4 h-4 text-gray-500" />
                            </button>
                        ) : null}
                    </div>
                </div>

                {/* Dropdown de resultados */}
                {isOpen && (
                    <div
                        ref={dropdownRef}
                        id="search-results"
                        role="listbox"
                        className={cn(
                            'absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg',
                            'max-h-[400px] overflow-y-auto z-50',
                            'animate-in fade-in-0 zoom-in-95 duration-200'
                        )}
                    >
                        {/* Mínimo de caracteres */}
                        {debouncedValue.length < 2 && (
                            <div className="p-4 text-center text-sm text-gray-500">
                                Digite pelo menos 2 caracteres para buscar
                            </div>
                        )}

                        {/* Loading */}
                        {isLoading && debouncedValue.length >= 2 && (
                            <div className="p-4 text-center">
                                <Loader2 className="w-6 h-6 text-primary-600 animate-spin mx-auto mb-2" />
                                <p className="text-sm text-gray-500">Buscando produtos...</p>
                            </div>
                        )}

                        {/* Nenhum resultado */}
                        {!isLoading &&
                            debouncedValue.length >= 2 &&
                            produtos &&
                            produtos.length === 0 && (
                                <div className="p-4 text-center">
                                    <p className="text-sm text-gray-600 mb-1">
                                        Nenhum produto encontrado para{' '}
                                        <span className="font-semibold">"{debouncedValue}"</span>
                                    </p>
                                    <p className="text-xs text-gray-500">
                                        Tente buscar por outro termo
                                    </p>
                                </div>
                            )}

                        {/* Lista de resultados */}
                        {!isLoading && produtos && produtos.length > 0 && (
                            <>
                                <div className="p-2 border-b border-gray-100 bg-gray-50">
                                    <p className="text-xs text-gray-600 font-medium px-2">
                                        {produtos.length} {produtos.length === 1 ? 'resultado' : 'resultados'} encontrado{produtos.length === 1 ? '' : 's'}
                                    </p>
                                </div>

                                <ul className="py-1">
                                    {produtos.map((produto, index) => (
                                        <li
                                            key={produto.id}
                                            role="option"
                                            aria-selected={selectedIndex === index}
                                        >
                                            <button
                                                onClick={() => handleSelectProduct(produto)}
                                                onMouseEnter={() => setSelectedIndex(index)}
                                                className={cn(
                                                    'w-full px-4 py-3 flex items-start gap-3 hover:bg-gray-50 transition-colors text-left',
                                                    selectedIndex === index && 'bg-primary-50 hover:bg-primary-100'
                                                )}
                                            >
                                                {/* Imagem do produto */}
                                                {produto.imagem_url ? (
                                                    <img
                                                        src={produto.imagem_url}
                                                        alt={produto.nome}
                                                        className="w-12 h-12 object-cover rounded-md flex-shrink-0"
                                                    />
                                                ) : (
                                                    <div className="w-12 h-12 bg-gray-200 rounded-md flex items-center justify-center flex-shrink-0">
                                                        <Search className="w-6 h-6 text-gray-400" />
                                                    </div>
                                                )}

                                                {/* Informações do produto */}
                                                <div className="flex-1 min-w-0">
                                                    <h4 className="text-sm font-semibold text-gray-900 mb-0.5 truncate">
                                                        {highlightTerm(produto.nome, debouncedValue)}
                                                    </h4>

                                                    {produto.descricao && (
                                                        <p className="text-xs text-gray-600 line-clamp-1 mb-1">
                                                            {highlightTerm(produto.descricao, debouncedValue)}
                                                        </p>
                                                    )}

                                                    <div className="flex items-center gap-2">
                                                        <span className="text-sm font-medium text-primary-600">
                                                            {getFaixaPrecos(produto)}
                                                        </span>

                                                        {!produto.disponivel && (
                                                            <span className="text-xs px-2 py-0.5 bg-red-100 text-red-700 rounded-full">
                                                                Indisponível
                                                            </span>
                                                        )}
                                                    </div>
                                                </div>
                                            </button>
                                        </li>
                                    ))}
                                </ul>
                            </>
                        )}
                    </div>
                )}
            </div>
        )
    }
)

SearchBar.displayName = 'SearchBar'

export default SearchBar
