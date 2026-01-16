import { useEffect, useRef } from 'react'
import type { ReactNode } from 'react'
import { createPortal } from 'react-dom'
import { X } from 'lucide-react'
import { cn } from '@/lib/utils'
import Button from './Button'

interface ModalProps {
  /**
   * Controla se o modal está aberto ou fechado
   */
  isOpen: boolean

  /**
   * Callback chamado quando o modal deve ser fechado
   */
  onClose: () => void

  /**
   * Título do modal (exibido no header)
   */
  title?: string

  /**
   * Conteúdo do modal
   */
  children: ReactNode

  /**
   * Tamanho do modal
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'

  /**
   * Permite fechar clicando no overlay (fora do modal)
   * @default true
   */
  closeOnOverlayClick?: boolean

  /**
   * Permite fechar pressionando ESC
   * @default true
   */
  closeOnEsc?: boolean

  /**
   * Mostra o botão X no header
   * @default true
   */
  showCloseButton?: boolean

  /**
   * Footer customizado do modal
   */
  footer?: ReactNode

  /**
   * Classes CSS adicionais para o container do modal
   */
  className?: string

  /**
   * Classes CSS adicionais para o conteúdo interno
   */
  contentClassName?: string
}

function Modal({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  closeOnOverlayClick = true,
  closeOnEsc = true,
  showCloseButton = true,
  footer,
  className,
  contentClassName,
}: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null)
  const previousActiveElement = useRef<HTMLElement | null>(null)

  // Bloquear scroll do body quando modal está aberto
  useEffect(() => {
    if (isOpen) {
      // Salvar posição atual do scroll
      const scrollY = window.scrollY
      document.body.style.position = 'fixed'
      document.body.style.top = `-${scrollY}px`
      document.body.style.width = '100%'

      return () => {
        // Restaurar scroll ao fechar
        document.body.style.position = ''
        document.body.style.top = ''
        document.body.style.width = ''
        window.scrollTo(0, scrollY)
      }
    }
  }, [isOpen])

  // Fechar com ESC
  useEffect(() => {
    if (!isOpen || !closeOnEsc) return

    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }

    document.addEventListener('keydown', handleEsc)
    return () => document.removeEventListener('keydown', handleEsc)
  }, [isOpen, closeOnEsc, onClose])

  // Focar no modal quando abrir e implementar trap de foco
  useEffect(() => {
    if (isOpen && modalRef.current) {
      // Salvar elemento que tinha foco antes do modal abrir
      previousActiveElement.current = document.activeElement as HTMLElement

      // Focar no modal
      modalRef.current.focus()

      // Trap de foco: manter foco dentro do modal
      const handleTabKey = (e: KeyboardEvent) => {
        if (!modalRef.current) return

        const focusableElements = modalRef.current.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        )
        const firstElement = focusableElements[0] as HTMLElement
        const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement

        if (e.key === 'Tab') {
          if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault()
            lastElement?.focus()
          } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault()
            firstElement?.focus()
          }
        }
      }

      document.addEventListener('keydown', handleTabKey)
      return () => document.removeEventListener('keydown', handleTabKey)
    } else if (!isOpen && previousActiveElement.current) {
      // Retornar foco ao elemento que abriu o modal
      previousActiveElement.current.focus()
      previousActiveElement.current = null
    }
  }, [isOpen])

  // Handler para click no overlay
  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (closeOnOverlayClick && e.target === e.currentTarget) {
      onClose()
    }
  }

  // Tamanhos do modal
  const sizeStyles = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-full mx-4',
  }

  // Não renderizar nada se não estiver aberto
  if (!isOpen) return null

  // Renderizar modal usando Portal (fora da árvore DOM)
  return createPortal(
    <div
      className="fixed inset-0 z-50 overflow-y-auto"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black/50 transition-opacity duration-300 animate-in fade-in"
        onClick={handleOverlayClick}
      />

      {/* Container centralizado */}
      <div className="flex min-h-full items-center justify-center p-4">
        {/* Modal */}
        <div
          ref={modalRef}
          tabIndex={-1}
          className={cn(
            'relative w-full bg-white rounded-lg shadow-xl transition-all duration-300',
            'animate-in zoom-in-95 fade-in slide-in-from-bottom-4',
            sizeStyles[size],
            className
          )}
        >
          {/* Header */}
          {(title || showCloseButton) && (
            <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
              {title && (
                <h2
                  id="modal-title"
                  className="text-xl font-semibold text-gray-900"
                >
                  {title}
                </h2>
              )}
              {showCloseButton && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onClose}
                  className={cn(
                    'text-gray-400 hover:text-gray-600',
                    !title && 'absolute right-4 top-4'
                  )}
                  aria-label="Fechar modal"
                >
                  <X size={20} />
                </Button>
              )}
            </div>
          )}

          {/* Content */}
          <div className={cn('px-6 py-4', contentClassName)}>
            {children}
          </div>

          {/* Footer */}
          {footer && (
            <div className="px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-lg">
              {footer}
            </div>
          )}
        </div>
      </div>
    </div>,
    document.body
  )
}

export default Modal
