import { useState, useEffect } from 'react'
import { cn, formatarPreco } from '@/lib/utils'
import type { Produto, Ingrediente } from '@/types/cardapio.types'
import { Plus, Minus, X } from 'lucide-react'

interface IngredientesCustomizacaoProps {
  /**
   * Produto com lista de ingredientes
   */
  produto: Produto

  /**
   * Callback quando ingredientes são modificados
   */
  onChange?: (data: {
    ingredientesAdicionados: Ingrediente[]
    ingredientesRemovidos: number[]
    observacoes: string
    precoIngredientes: number
  }) => void

  /**
   * Classes CSS adicionais
   */
  className?: string
}

function IngredientesCustomizacao({
  produto,
  onChange,
  className,
}: IngredientesCustomizacaoProps) {
  // Estado dos ingredientes adicionados (extras)
  const [ingredientesAdicionados, setIngredientesAdicionados] = useState<Ingrediente[]>([])

  // Estado dos ingredientes removidos (IDs)
  const [ingredientesRemovidos, setIngredientesRemovidos] = useState<number[]>([])

  // Estado das observações
  const [observacoes, setObservacoes] = useState('')

  // Separar ingredientes padrão em obrigatórios e opcionais
  const ingredientesPadrao = produto.ingredientes || []
  const ingredientesObrigatorios = ingredientesPadrao.filter((pi) => pi.obrigatorio)
  const ingredientesOpcionais = ingredientesPadrao.filter((pi) => !pi.obrigatorio)

  // Lista de ingredientes adicionais disponíveis (mock - idealmente viria da API)
  // Para fins de teste, vamos criar alguns ingredientes extras
  const ingredientesExtras: Ingrediente[] = [
    { id: 100, nome: 'Borda Recheada (Catupiry)', preco_adicional: 8.0, disponivel: true },
    { id: 101, nome: 'Borda Recheada (Cheddar)', preco_adicional: 8.0, disponivel: true },
    { id: 102, nome: 'Bacon', preco_adicional: 5.0, disponivel: true },
    { id: 103, nome: 'Azeitona Preta', preco_adicional: 3.0, disponivel: true },
    { id: 104, nome: 'Palmito', preco_adicional: 6.0, disponivel: true },
    { id: 105, nome: 'Rúcula', preco_adicional: 4.0, disponivel: true },
    { id: 106, nome: 'Tomate Seco', preco_adicional: 5.0, disponivel: true },
    { id: 107, nome: 'Orégano Extra', preco_adicional: 0.5, disponivel: true },
  ]

  // Calcular preço dos ingredientes
  const calcularPrecoIngredientes = () => {
    // Soma dos ingredientes adicionados
    const precoAdicionados = ingredientesAdicionados.reduce(
      (sum, ing) => sum + ing.preco_adicional,
      0
    )

    // Ingredientes removidos não afetam o preço (já estão inclusos no preço base)
    return precoAdicionados
  }

  // Notificar mudanças
  useEffect(() => {
    if (onChange) {
      onChange({
        ingredientesAdicionados,
        ingredientesRemovidos,
        observacoes,
        precoIngredientes: calcularPrecoIngredientes(),
      })
    }
  }, [ingredientesAdicionados, ingredientesRemovidos, observacoes])

  // Handler para adicionar ingrediente extra
  const handleAdicionarIngrediente = (ingrediente: Ingrediente) => {
    if (!ingredientesAdicionados.find((i) => i.id === ingrediente.id)) {
      setIngredientesAdicionados([...ingredientesAdicionados, ingrediente])
    }
  }

  // Handler para remover ingrediente extra
  const handleRemoverIngredienteExtra = (ingredienteId: number) => {
    setIngredientesAdicionados(
      ingredientesAdicionados.filter((i) => i.id !== ingredienteId)
    )
  }

  // Handler para toggle de ingrediente opcional (padrão)
  const handleToggleIngredienteOpcional = (ingredienteId: number) => {
    if (ingredientesRemovidos.includes(ingredienteId)) {
      // Remover da lista de removidos (voltar a incluir)
      setIngredientesRemovidos(ingredientesRemovidos.filter((id) => id !== ingredienteId))
    } else {
      // Adicionar à lista de removidos
      setIngredientesRemovidos([...ingredientesRemovidos, ingredienteId])
    }
  }

  const precoIngredientes = calcularPrecoIngredientes()

  return (
    <div className={cn('space-y-6', className)}>
      {/* Ingredientes Padrão Obrigatórios */}
      {ingredientesObrigatorios.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-gray-900 mb-3">
            Ingredientes Inclusos (Obrigatórios)
          </h4>
          <div className="space-y-2">
            {ingredientesObrigatorios.map((pi) => (
              <div
                key={pi.ingrediente.id}
                className="flex items-center gap-3 p-3 bg-gray-50 border border-gray-200 rounded-lg"
              >
                <div className="flex items-center justify-center w-5 h-5 rounded bg-gray-300">
                  <span className="text-xs text-gray-600">✓</span>
                </div>
                <span className="flex-1 text-sm text-gray-700">
                  {pi.ingrediente.nome}
                </span>
                <span className="text-xs text-gray-500 italic">Obrigatório</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Ingredientes Padrão Opcionais */}
      {ingredientesOpcionais.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-gray-900 mb-3">
            Ingredientes Inclusos (Opcionais)
          </h4>
          <p className="text-xs text-gray-600 mb-3">
            Desmarque os ingredientes que você NÃO deseja
          </p>
          <div className="space-y-2">
            {ingredientesOpcionais.map((pi) => {
              const isRemovido = ingredientesRemovidos.includes(pi.ingrediente.id)
              return (
                <button
                  key={pi.ingrediente.id}
                  type="button"
                  onClick={() => handleToggleIngredienteOpcional(pi.ingrediente.id)}
                  className={cn(
                    'w-full flex items-center gap-3 p-3 border-2 rounded-lg transition-all',
                    'hover:border-primary-300 focus:outline-none focus:ring-2 focus:ring-primary-500',
                    isRemovido
                      ? 'bg-gray-50 border-gray-200 opacity-60'
                      : 'bg-white border-green-200'
                  )}
                >
                  <div
                    className={cn(
                      'flex items-center justify-center w-5 h-5 rounded border-2 transition-all',
                      isRemovido
                        ? 'border-gray-300 bg-white'
                        : 'border-green-600 bg-green-600'
                    )}
                  >
                    {!isRemovido && <span className="text-xs text-white">✓</span>}
                  </div>
                  <span
                    className={cn(
                      'flex-1 text-left text-sm',
                      isRemovido ? 'text-gray-400 line-through' : 'text-gray-700'
                    )}
                  >
                    {pi.ingrediente.nome}
                  </span>
                  {isRemovido && (
                    <X size={16} className="text-red-500" />
                  )}
                </button>
              )
            })}
          </div>
        </div>
      )}

      {/* Ingredientes Adicionais */}
      <div>
        <h4 className="text-sm font-semibold text-gray-900 mb-3">
          Ingredientes Adicionais
        </h4>
        <p className="text-xs text-gray-600 mb-3">
          Adicione ingredientes extras (valores adicionais serão cobrados)
        </p>

        {/* Lista de ingredientes disponíveis para adicionar */}
        <div className="space-y-2 mb-4">
          {ingredientesExtras
            .filter((ing) => !ingredientesAdicionados.find((i) => i.id === ing.id))
            .map((ingrediente) => (
              <button
                key={ingrediente.id}
                type="button"
                onClick={() => handleAdicionarIngrediente(ingrediente)}
                disabled={!ingrediente.disponivel}
                className={cn(
                  'w-full flex items-center gap-3 p-3 border-2 border-gray-200 rounded-lg transition-all',
                  'hover:border-primary-300 bg-white focus:outline-none focus:ring-2 focus:ring-primary-500',
                  !ingrediente.disponivel && 'opacity-50 cursor-not-allowed'
                )}
              >
                <div className="flex items-center justify-center w-5 h-5 rounded border-2 border-gray-300 bg-white">
                  <Plus size={14} className="text-gray-400" />
                </div>
                <span className="flex-1 text-left text-sm text-gray-700">
                  {ingrediente.nome}
                </span>
                <span className="text-sm font-semibold text-primary-600">
                  + {formatarPreco(ingrediente.preco_adicional)}
                </span>
              </button>
            ))}
        </div>

        {/* Lista de ingredientes adicionados */}
        {ingredientesAdicionados.length > 0 && (
          <div className="border-t border-gray-200 pt-4">
            <p className="text-xs font-medium text-gray-700 mb-2">
              Ingredientes adicionados:
            </p>
            <div className="space-y-2">
              {ingredientesAdicionados.map((ingrediente) => (
                <div
                  key={ingrediente.id}
                  className="flex items-center gap-3 p-3 bg-green-50 border border-green-200 rounded-lg"
                >
                  <div className="flex items-center justify-center w-5 h-5 rounded bg-green-600">
                    <Plus size={14} className="text-white" />
                  </div>
                  <span className="flex-1 text-sm text-gray-700">
                    {ingrediente.nome}
                  </span>
                  <span className="text-sm font-semibold text-green-700">
                    + {formatarPreco(ingrediente.preco_adicional)}
                  </span>
                  <button
                    type="button"
                    onClick={() => handleRemoverIngredienteExtra(ingrediente.id)}
                    className="p-1 hover:bg-red-100 rounded transition-colors"
                    aria-label={`Remover ${ingrediente.nome}`}
                  >
                    <Minus size={16} className="text-red-600" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Campo de Observações */}
      <div>
        <label
          htmlFor="observacoes"
          className="block text-sm font-semibold text-gray-900 mb-2"
        >
          Observações
        </label>
        <textarea
          id="observacoes"
          value={observacoes}
          onChange={(e) => setObservacoes(e.target.value)}
          placeholder="Ex: Sem cebola, bem assada, etc."
          rows={3}
          maxLength={200}
          className={cn(
            'w-full px-4 py-3 border-2 border-gray-200 rounded-lg',
            'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'resize-none text-sm text-gray-700 placeholder-gray-400',
            'transition-all'
          )}
        />
        <p className="text-xs text-gray-500 mt-1">
          {observacoes.length}/200 caracteres
        </p>
      </div>

      {/* Resumo de Preço dos Ingredientes */}
      {precoIngredientes > 0 && (
        <div className="border-t border-gray-200 pt-4">
          <div className="flex items-center justify-between p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <span className="text-sm font-medium text-blue-900">
              Valor dos ingredientes adicionais:
            </span>
            <span className="text-lg font-bold text-blue-700">
              + {formatarPreco(precoIngredientes)}
            </span>
          </div>
        </div>
      )}
    </div>
  )
}

export default IngredientesCustomizacao
