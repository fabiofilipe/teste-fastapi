import { useState, useRef, useEffect, cloneElement, isValidElement } from 'react'
import type { ReactElement, ReactNode } from 'react'
import { createPortal } from 'react-dom'
import { cn } from '@/lib/utils'

interface TooltipProps {
  /**
   * Conteúdo do tooltip
   */
  content: ReactNode

  /**
   * Elemento que dispara o tooltip (deve aceitar ref e event handlers)
   */
  children: ReactElement

  /**
   * Posição do tooltip em relação ao elemento
   * @default 'top'
   */
  position?: 'top' | 'bottom' | 'left' | 'right'

  /**
   * Delay em ms antes de mostrar o tooltip
   * @default 200
   */
  delay?: number

  /**
   * Desabilita o tooltip
   * @default false
   */
  disabled?: boolean

  /**
   * Classes CSS adicionais para o container do tooltip
   */
  className?: string
}

function Tooltip({
  content,
  children,
  position = 'top',
  delay = 200,
  disabled = false,
  className,
}: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false)
  const [coords, setCoords] = useState({ top: 0, left: 0 })
  const triggerRef = useRef<HTMLElement>(null)
  const tooltipRef = useRef<HTMLDivElement>(null)
  const timeoutRef = useRef<NodeJS.Timeout>()

  // Calcular posição do tooltip
  const updatePosition = () => {
    if (!triggerRef.current || !tooltipRef.current) return

    const triggerRect = triggerRef.current.getBoundingClientRect()
    const tooltipRect = tooltipRef.current.getBoundingClientRect()
    const offset = 8 // Espaçamento entre elemento e tooltip

    let top = 0
    let left = 0

    switch (position) {
      case 'top':
        top = triggerRect.top - tooltipRect.height - offset
        left = triggerRect.left + triggerRect.width / 2 - tooltipRect.width / 2
        break
      case 'bottom':
        top = triggerRect.bottom + offset
        left = triggerRect.left + triggerRect.width / 2 - tooltipRect.width / 2
        break
      case 'left':
        top = triggerRect.top + triggerRect.height / 2 - tooltipRect.height / 2
        left = triggerRect.left - tooltipRect.width - offset
        break
      case 'right':
        top = triggerRect.top + triggerRect.height / 2 - tooltipRect.height / 2
        left = triggerRect.right + offset
        break
    }

    // Ajustar se sair da tela
    const padding = 8
    if (left < padding) left = padding
    if (left + tooltipRect.width > window.innerWidth - padding) {
      left = window.innerWidth - tooltipRect.width - padding
    }
    if (top < padding) top = padding
    if (top + tooltipRect.height > window.innerHeight - padding) {
      top = window.innerHeight - tooltipRect.height - padding
    }

    setCoords({ top, left })
  }

  // Mostrar tooltip com delay
  const handleMouseEnter = () => {
    if (disabled) return
    timeoutRef.current = setTimeout(() => {
      setIsVisible(true)
    }, delay)
  }

  // Esconder tooltip imediatamente
  const handleMouseLeave = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
    }
    setIsVisible(false)
  }

  // Atualizar posição quando visível
  useEffect(() => {
    if (isVisible) {
      updatePosition()
      // Recalcular ao redimensionar
      window.addEventListener('resize', updatePosition)
      window.addEventListener('scroll', updatePosition, true)
      return () => {
        window.removeEventListener('resize', updatePosition)
        window.removeEventListener('scroll', updatePosition, true)
      }
    }
  }, [isVisible])

  // Cleanup timeout ao desmontar
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [])

  // Classes do tooltip
  const positionStyles = {
    top: 'animate-in fade-in slide-in-from-bottom-1',
    bottom: 'animate-in fade-in slide-in-from-top-1',
    left: 'animate-in fade-in slide-in-from-right-1',
    right: 'animate-in fade-in slide-in-from-left-1',
  }

  // Clonar children para adicionar props
  const trigger = isValidElement(children)
    ? cloneElement(children, {
        ref: triggerRef,
        onMouseEnter: handleMouseEnter,
        onMouseLeave: handleMouseLeave,
        onFocus: handleMouseEnter,
        onBlur: handleMouseLeave,
        'aria-describedby': isVisible ? 'tooltip' : undefined,
      } as any)
    : children

  return (
    <>
      {trigger}
      {isVisible &&
        !disabled &&
        createPortal(
          <div
            ref={tooltipRef}
            id="tooltip"
            role="tooltip"
            className={cn(
              'fixed z-[100] px-3 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-lg',
              'max-w-xs pointer-events-none',
              'duration-150',
              positionStyles[position],
              className
            )}
            style={{
              top: `${coords.top}px`,
              left: `${coords.left}px`,
            }}
          >
            {content}
            {/* Seta do tooltip */}
            <div
              className={cn(
                'absolute w-2 h-2 bg-gray-900 rotate-45',
                position === 'top' && 'bottom-[-4px] left-1/2 -translate-x-1/2',
                position === 'bottom' && 'top-[-4px] left-1/2 -translate-x-1/2',
                position === 'left' && 'right-[-4px] top-1/2 -translate-y-1/2',
                position === 'right' && 'left-[-4px] top-1/2 -translate-y-1/2'
              )}
            />
          </div>,
          document.body
        )}
    </>
  )
}

export default Tooltip
