import { CarrinhoProvider } from './contexts/CarrinhoContext'
import Cardapio from './pages/Cardapio'

// ============================================================================
// APP CONTENT
// ============================================================================

function AppContent() {
  return <Cardapio />
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
