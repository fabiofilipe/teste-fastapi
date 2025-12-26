import { CarrinhoProvider } from './contexts/CarrinhoContext'
import TestModal from './TestModal'

// ============================================================================
// APP CONTENT
// ============================================================================

function AppContent() {
  return <TestModal />
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
