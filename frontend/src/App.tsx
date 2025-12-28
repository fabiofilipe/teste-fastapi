import { CarrinhoProvider } from './contexts/CarrinhoContext'
import TestCarrinho from './TestCarrinho'

// ============================================================================
// APP CONTENT
// ============================================================================

function AppContent() {
  return <TestCarrinho />
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
