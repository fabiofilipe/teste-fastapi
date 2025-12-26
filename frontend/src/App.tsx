import { CarrinhoProvider } from './contexts/CarrinhoContext'
import TestVariacao from './TestVariacao'

// ============================================================================
// APP CONTENT
// ============================================================================

function AppContent() {
  return <TestVariacao />
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
