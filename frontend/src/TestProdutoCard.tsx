import ProdutoCard from '@/components/cardapio/ProdutoCard'
import type { Produto } from '@/types/cardapio.types'
import Layout from '@/components/layout/Layout'

// Dados de teste
const produtosMock: Produto[] = [
  {
    id: 1,
    nome: 'Pizza Margherita',
    descricao: 'Molho de tomate, mussarela, manjericão fresco e azeite',
    imagem_url: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=300&fit=crop',
    categoria_id: 1,
    disponivel: true,
    variacoes: [
      { id: 1, tamanho: 'Pequena', preco: 25.9, disponivel: true },
      { id: 2, tamanho: 'Média', preco: 35.9, disponivel: true },
      { id: 3, tamanho: 'Grande', preco: 45.9, disponivel: true },
      { id: 4, tamanho: 'Gigante', preco: 55.9, disponivel: true },
    ],
    ingredientes: [
      {
        ingrediente: { id: 1, nome: 'Mussarela', preco_adicional: 5, disponivel: true },
        obrigatorio: true,
      },
      {
        ingrediente: { id: 2, nome: 'Manjericão', preco_adicional: 0, disponivel: true },
        obrigatorio: true,
      },
    ],
  },
  {
    id: 2,
    nome: 'Pizza Calabresa',
    descricao: 'Calabresa, cebola, azeitona e mussarela',
    imagem_url: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400&h=300&fit=crop',
    categoria_id: 1,
    disponivel: true,
    variacoes: [
      { id: 5, tamanho: 'Média', preco: 38.9, disponivel: true },
      { id: 6, tamanho: 'Grande', preco: 48.9, disponivel: true },
    ],
    ingredientes: [
      {
        ingrediente: { id: 3, nome: 'Calabresa', preco_adicional: 8, disponivel: true },
        obrigatorio: true,
      },
      {
        ingrediente: { id: 4, nome: 'Cebola', preco_adicional: 2, disponivel: true },
        obrigatorio: false,
      },
    ],
  },
  {
    id: 3,
    nome: 'Pizza Portuguesa',
    descricao: 'Presunto, ovos, cebola, azeitona, ervilha e mussarela',
    imagem_url: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop',
    categoria_id: 1,
    disponivel: false,
    variacoes: [
      { id: 7, tamanho: 'Grande', preco: 52.9, disponivel: false },
    ],
    ingredientes: [],
  },
  {
    id: 4,
    nome: 'Pizza Quatro Queijos',
    descricao: 'Mussarela, provolone, parmesão e gorgonzola',
    imagem_url: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop',
    categoria_id: 1,
    disponivel: true,
    variacoes: [
      { id: 8, tamanho: 'Grande', preco: 49.9, disponivel: true },
    ],
    ingredientes: [
      {
        ingrediente: { id: 5, nome: 'Mussarela', preco_adicional: 5, disponivel: true },
        obrigatorio: true,
      },
      {
        ingrediente: { id: 6, nome: 'Provolone', preco_adicional: 6, disponivel: true },
        obrigatorio: true,
      },
      {
        ingrediente: { id: 7, nome: 'Parmesão', preco_adicional: 6, disponivel: true },
        obrigatorio: true,
      },
      {
        ingrediente: { id: 8, nome: 'Gorgonzola', preco_adicional: 7, disponivel: true },
        obrigatorio: true,
      },
    ],
  },
  {
    id: 5,
    nome: 'Pizza Vegana',
    descricao: 'Tomate, cogumelos, pimentão, rúcula e queijo vegano',
    imagem_url: null, // Teste do placeholder
    categoria_id: 1,
    disponivel: true,
    variacoes: [
      { id: 9, tamanho: 'Média', preco: 42.9, disponivel: true },
      { id: 10, tamanho: 'Grande', preco: 52.9, disponivel: true },
    ],
    ingredientes: [
      {
        ingrediente: { id: 9, nome: 'Queijo vegano', preco_adicional: 10, disponivel: true },
        obrigatorio: true,
      },
    ],
  },
  {
    id: 6,
    nome: 'Pizza Especial da Casa',
    descricao: null, // Teste sem descrição
    imagem_url: 'https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f?w=400&h=300&fit=crop',
    categoria_id: 1,
    disponivel: true,
    variacoes: [],
    ingredientes: [],
  },
]

function TestProdutoCard() {
  const handleVerDetalhes = (produto: Produto) => {
    console.log('Ver detalhes do produto:', produto)
    alert(`Ver detalhes: ${produto.nome}`)
  }

  return (
    <Layout maxWidth="7xl">
      <div className="py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Teste: ProdutoCard Component
          </h1>
          <p className="text-gray-600">
            Testando o componente ProdutoCard com diferentes cenários
          </p>
        </div>

        {/* Grid responsivo de produtos */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {produtosMock.map((produto) => (
            <ProdutoCard
              key={produto.id}
              produto={produto}
              onVerDetalhes={handleVerDetalhes}
            />
          ))}
        </div>

        {/* Legenda dos cenários testados */}
        <div className="mt-12 p-6 bg-gray-50 rounded-lg">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Cenários Testados:
          </h2>
          <ul className="space-y-2 text-sm text-gray-700">
            <li>
              <strong>Pizza Margherita:</strong> Produto disponível com 4
              variações de preço (R$ 25,90 - R$ 55,90)
            </li>
            <li>
              <strong>Pizza Calabresa:</strong> Produto disponível com 2
              variações (R$ 38,90 - R$ 48,90)
            </li>
            <li>
              <strong>Pizza Portuguesa:</strong> Produto INDISPONÍVEL (overlay
              com badge)
            </li>
            <li>
              <strong>Pizza Quatro Queijos:</strong> Produto com preço único (R$
              49,90)
            </li>
            <li>
              <strong>Pizza Vegana:</strong> Produto sem imagem (placeholder
              gerado)
            </li>
            <li>
              <strong>Pizza Especial da Casa:</strong> Produto sem descrição e
              sem variações (badge de aviso)
            </li>
          </ul>
        </div>

        {/* Instruções */}
        <div className="mt-6 p-6 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">
            Instruções de Teste:
          </h3>
          <ul className="space-y-1 text-sm text-blue-800">
            <li>✓ Hover nos cards disponíveis (elevação e escala da imagem)</li>
            <li>✓ Clique em "Ver detalhes" (alert com nome do produto)</li>
            <li>✓ Teste em diferentes tamanhos de tela (responsividade)</li>
            <li>✓ Verifique lazy loading das imagens (scroll)</li>
            <li>✓ Badges de status (disponível, indisponível, sem variações)</li>
            <li>✓ Formatação de preços em Real (R$)</li>
            <li>✓ Line-clamp em nome e descrição (máx 2 linhas)</li>
          </ul>
        </div>
      </div>
    </Layout>
  )
}

export default TestProdutoCard
