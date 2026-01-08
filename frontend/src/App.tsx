import { CarrinhoProvider } from './contexts/CarrinhoContext'
import TestSearchBar from './TestSearchBar'

// ============================================================================
// APP CONTENT
// ============================================================================

function AppContent() {
  return <TestSearchBar />
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
