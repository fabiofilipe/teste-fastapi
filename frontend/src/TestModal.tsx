import { useState } from 'react'
import Layout from '@/components/layout/Layout'
import Modal from '@/components/common/Modal'
import Button from '@/components/common/Button'
import Card from '@/components/common/Card'
import Badge from '@/components/common/Badge'
import { Check, X, AlertTriangle } from 'lucide-react'

function TestModal() {
  // Estados para controlar cada modal
  const [isModalSimpleOpen, setIsModalSimpleOpen] = useState(false)
  const [isModalWithFooterOpen, setIsModalWithFooterOpen] = useState(false)
  const [isModalLargeOpen, setIsModalLargeOpen] = useState(false)
  const [isModalFullOpen, setIsModalFullOpen] = useState(false)
  const [isModalNoCloseOpen, setIsModalNoCloseOpen] = useState(false)
  const [isModalConfirmOpen, setIsModalConfirmOpen] = useState(false)

  return (
    <Layout maxWidth="7xl">
      <div className="py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Teste: Modal Component
          </h1>
          <p className="text-gray-600">
            Testando o componente Modal com diferentes configurações
          </p>
        </div>

        {/* Grid de botões para abrir modais */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {/* Modal Simples */}
          <Card>
            <h3 className="font-semibold text-gray-900 mb-2">Modal Simples (SM)</h3>
            <p className="text-sm text-gray-600 mb-4">
              Modal pequeno com título e conteúdo básico
            </p>
            <Button
              variant="primary"
              onClick={() => setIsModalSimpleOpen(true)}
              className="w-full"
            >
              Abrir Modal Simples
            </Button>
          </Card>

          {/* Modal com Footer */}
          <Card>
            <h3 className="font-semibold text-gray-900 mb-2">Modal com Footer (MD)</h3>
            <p className="text-sm text-gray-600 mb-4">
              Modal médio com título, conteúdo e footer customizado
            </p>
            <Button
              variant="secondary"
              onClick={() => setIsModalWithFooterOpen(true)}
              className="w-full"
            >
              Abrir Modal com Footer
            </Button>
          </Card>

          {/* Modal Large */}
          <Card>
            <h3 className="font-semibold text-gray-900 mb-2">Modal Grande (LG)</h3>
            <p className="text-sm text-gray-600 mb-4">
              Modal grande com muito conteúdo e scroll interno
            </p>
            <Button
              variant="outline"
              onClick={() => setIsModalLargeOpen(true)}
              className="w-full"
            >
              Abrir Modal Grande
            </Button>
          </Card>

          {/* Modal Full */}
          <Card>
            <h3 className="font-semibold text-gray-900 mb-2">Modal Full Width (XL)</h3>
            <p className="text-sm text-gray-600 mb-4">
              Modal extra grande ocupando quase toda a tela
            </p>
            <Button
              variant="primary"
              onClick={() => setIsModalFullOpen(true)}
              className="w-full"
            >
              Abrir Modal Full
            </Button>
          </Card>

          {/* Modal sem close button */}
          <Card>
            <h3 className="font-semibold text-gray-900 mb-2">Modal Restrito</h3>
            <p className="text-sm text-gray-600 mb-4">
              Sem botão X, não fecha ao clicar fora ou ESC
            </p>
            <Button
              variant="danger"
              onClick={() => setIsModalNoCloseOpen(true)}
              className="w-full"
            >
              Abrir Modal Restrito
            </Button>
          </Card>

          {/* Modal de confirmação */}
          <Card>
            <h3 className="font-semibold text-gray-900 mb-2">Modal de Confirmação</h3>
            <p className="text-sm text-gray-600 mb-4">
              Modal estilo confirmação com ações
            </p>
            <Button
              variant="outline"
              onClick={() => setIsModalConfirmOpen(true)}
              className="w-full"
            >
              Abrir Confirmação
            </Button>
          </Card>
        </div>

        {/* Instruções */}
        <Card className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Instruções de Teste:
          </h2>
          <div className="space-y-2 text-sm text-gray-700">
            <div className="flex items-start gap-2">
              <Check size={16} className="text-green-600 mt-0.5 flex-shrink-0" />
              <span>Tente fechar com <kbd className="px-1 py-0.5 bg-gray-200 rounded text-xs">ESC</kbd></span>
            </div>
            <div className="flex items-start gap-2">
              <Check size={16} className="text-green-600 mt-0.5 flex-shrink-0" />
              <span>Tente clicar fora do modal (no overlay escuro)</span>
            </div>
            <div className="flex items-start gap-2">
              <Check size={16} className="text-green-600 mt-0.5 flex-shrink-0" />
              <span>Clique no botão X no canto superior direito</span>
            </div>
            <div className="flex items-start gap-2">
              <Check size={16} className="text-green-600 mt-0.5 flex-shrink-0" />
              <span>Observe que o scroll da página é bloqueado quando modal está aberto</span>
            </div>
            <div className="flex items-start gap-2">
              <Check size={16} className="text-green-600 mt-0.5 flex-shrink-0" />
              <span>Teste a responsividade em diferentes tamanhos de tela</span>
            </div>
            <div className="flex items-start gap-2">
              <AlertTriangle size={16} className="text-yellow-600 mt-0.5 flex-shrink-0" />
              <span>O Modal Restrito só fecha pelo botão "Fechar" interno</span>
            </div>
          </div>
        </Card>

        {/* Features testadas */}
        <Card>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Features Testadas:
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="flex items-start gap-2">
              <Badge variant="success" size="sm">✓</Badge>
              <span className="text-sm text-gray-700">Overlay com backdrop</span>
            </div>
            <div className="flex items-start gap-2">
              <Badge variant="success" size="sm">✓</Badge>
              <span className="text-sm text-gray-700">Animações de entrada/saída</span>
            </div>
            <div className="flex items-start gap-2">
              <Badge variant="success" size="sm">✓</Badge>
              <span className="text-sm text-gray-700">Fechar com ESC</span>
            </div>
            <div className="flex items-start gap-2">
              <Badge variant="success" size="sm">✓</Badge>
              <span className="text-sm text-gray-700">Fechar clicando fora</span>
            </div>
            <div className="flex items-start gap-2">
              <Badge variant="success" size="sm">✓</Badge>
              <span className="text-sm text-gray-700">Botão X no header</span>
            </div>
            <div className="flex items-start gap-2">
              <Badge variant="success" size="sm">✓</Badge>
              <span className="text-sm text-gray-700">Bloquear scroll do body</span>
            </div>
            <div className="flex items-start gap-2">
              <Badge variant="success" size="sm">✓</Badge>
              <span className="text-sm text-gray-700">5 tamanhos (sm, md, lg, xl, full)</span>
            </div>
            <div className="flex items-start gap-2">
              <Badge variant="success" size="sm">✓</Badge>
              <span className="text-sm text-gray-700">Footer customizável</span>
            </div>
            <div className="flex items-start gap-2">
              <Badge variant="success" size="sm">✓</Badge>
              <span className="text-sm text-gray-700">Portal (renderiza no body)</span>
            </div>
            <div className="flex items-start gap-2">
              <Badge variant="success" size="sm">✓</Badge>
              <span className="text-sm text-gray-700">Acessibilidade (ARIA)</span>
            </div>
          </div>
        </Card>
      </div>

      {/* ============================================================================ */}
      {/* MODALS */}
      {/* ============================================================================ */}

      {/* Modal Simples */}
      <Modal
        isOpen={isModalSimpleOpen}
        onClose={() => setIsModalSimpleOpen(false)}
        title="Modal Simples"
        size="sm"
      >
        <p className="text-gray-600">
          Este é um modal simples com tamanho pequeno (SM). Você pode fechá-lo
          clicando no X, pressionando ESC ou clicando fora do modal.
        </p>
      </Modal>

      {/* Modal com Footer */}
      <Modal
        isOpen={isModalWithFooterOpen}
        onClose={() => setIsModalWithFooterOpen(false)}
        title="Modal com Footer"
        size="md"
        footer={
          <div className="flex justify-end gap-2">
            <Button
              variant="outline"
              onClick={() => setIsModalWithFooterOpen(false)}
            >
              Cancelar
            </Button>
            <Button
              variant="primary"
              onClick={() => {
                alert('Ação confirmada!')
                setIsModalWithFooterOpen(false)
              }}
            >
              Confirmar
            </Button>
          </div>
        }
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            Este modal tem um footer customizado com botões de ação.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              <strong>Dica:</strong> Use o footer para ações como "Salvar",
              "Cancelar", "Confirmar", etc.
            </p>
          </div>
        </div>
      </Modal>

      {/* Modal Large com Scroll */}
      <Modal
        isOpen={isModalLargeOpen}
        onClose={() => setIsModalLargeOpen(false)}
        title="Modal Grande com Conteúdo Extenso"
        size="lg"
        footer={
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-500">
              Role para ver todo o conteúdo
            </span>
            <Button variant="primary" onClick={() => setIsModalLargeOpen(false)}>
              Fechar
            </Button>
          </div>
        }
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            Este é um modal grande (LG) com muito conteúdo. O modal tem scroll
            interno quando o conteúdo é maior que a tela.
          </p>

          {/* Conteúdo longo para demonstrar scroll */}
          {Array.from({ length: 10 }).map((_, i) => (
            <Card key={i} variant="outlined" padding="sm">
              <h4 className="font-semibold text-gray-900 mb-1">
                Seção {i + 1}
              </h4>
              <p className="text-sm text-gray-600">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </p>
            </Card>
          ))}
        </div>
      </Modal>

      {/* Modal Full Width */}
      <Modal
        isOpen={isModalFullOpen}
        onClose={() => setIsModalFullOpen(false)}
        title="Modal Extra Grande (XL)"
        size="xl"
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            Este modal usa o tamanho XL, ocupando quase toda a largura da tela.
            Ideal para formulários extensos ou tabelas grandes.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <Card key={i}>
                <h4 className="font-semibold text-gray-900 mb-2">Card {i + 1}</h4>
                <p className="text-sm text-gray-600">
                  Demonstração de grid dentro do modal XL.
                </p>
              </Card>
            ))}
          </div>
        </div>
      </Modal>

      {/* Modal Restrito (sem close externo) */}
      <Modal
        isOpen={isModalNoCloseOpen}
        onClose={() => setIsModalNoCloseOpen(false)}
        title="Modal Restrito"
        size="md"
        showCloseButton={false}
        closeOnOverlayClick={false}
        closeOnEsc={false}
      >
        <div className="space-y-4">
          <div className="flex items-start gap-3 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <AlertTriangle className="text-yellow-600 flex-shrink-0" size={20} />
            <div>
              <p className="font-medium text-yellow-900 mb-1">Atenção!</p>
              <p className="text-sm text-yellow-800">
                Este modal não pode ser fechado clicando fora, pressionando ESC
                ou pelo botão X. Você deve usar o botão abaixo.
              </p>
            </div>
          </div>
          <p className="text-gray-600">
            Use este padrão para ações críticas que exigem decisão explícita do
            usuário.
          </p>
          <Button
            variant="primary"
            onClick={() => setIsModalNoCloseOpen(false)}
            className="w-full"
          >
            Fechar Modal
          </Button>
        </div>
      </Modal>

      {/* Modal de Confirmação */}
      <Modal
        isOpen={isModalConfirmOpen}
        onClose={() => setIsModalConfirmOpen(false)}
        size="sm"
      >
        <div className="text-center space-y-4">
          <div className="mx-auto w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
            <X className="text-red-600" size={24} />
          </div>
          <h3 className="text-lg font-semibold text-gray-900">
            Confirmar exclusão
          </h3>
          <p className="text-gray-600">
            Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita.
          </p>
          <div className="flex gap-3 pt-2">
            <Button
              variant="outline"
              onClick={() => setIsModalConfirmOpen(false)}
              className="flex-1"
            >
              Cancelar
            </Button>
            <Button
              variant="danger"
              onClick={() => {
                alert('Item excluído!')
                setIsModalConfirmOpen(false)
              }}
              className="flex-1"
            >
              Excluir
            </Button>
          </div>
        </div>
      </Modal>
    </Layout>
  )
}

export default TestModal
