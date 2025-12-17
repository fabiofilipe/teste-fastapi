interface FooterProps {
  /**
   * Ano do copyright (opcional, padrão: ano atual)
   */
  year?: number
}

const Footer = ({ year }: FooterProps) => {
  const currentYear = year || new Date().getFullYear()

  return (
    <footer className="bg-gray-100 border-t border-gray-200">
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-6">
        <div className="flex flex-col items-center justify-center gap-2 text-sm text-gray-600">
          <p className="text-center">
            Pizzaria © {currentYear} - Todos os direitos reservados
          </p>
          <p className="text-xs text-gray-500">
            Feito com ❤️ usando React + FastAPI
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
