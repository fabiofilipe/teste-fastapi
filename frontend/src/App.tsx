import { CarrinhoProvider } from './contexts/CarrinhoContext'
import TestProdutoCard from './TestProdutoCard'

// ============================================================================
// APP CONTENT
// ============================================================================

function AppContent() {
  return <TestProdutoCard />
}

// ============================================================================
// APP WRAPPER (com CarrinhoProvider)
// ============================================================================

function App() {
  return (
    <CarrinhoProvider>
      <AppContent />
    </CarrinhoProvider>
  )
}

export default App
