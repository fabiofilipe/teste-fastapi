# PLANO DE IMPLEMENTAÇÃO - FRONTEND DO CARDÁPIO

**Data de Criação:** 13/12/2025
**Última Atualização:** 26/12/2025 BRT
**Fase:** 1.3 - Sistema de Categorias e Cardápio Dinâmico
**Objetivo:** Criar interface completa de visualização e compra de produtos

**Progresso Geral:** Sprint 3 em progresso - 67% (40%)
**Sprint Atual:** Sprint 3 - Listagem de Produtos [EM PROGRESSO]
**Próxima Etapa:** Etapa 3.3 - Página de Cardápio

---

## ÍNDICE

1. [Stack Tecnológica](#stack-tecnológica)
2. [Estrutura de Diretórios](#estrutura-de-diretórios)
3. [Componentes Principais](#componentes-principais)
4. [Gerenciamento de Estado](#gerenciamento-de-estado)
5. [Integração com API](#integração-com-api)
6. [Fluxo de Implementação](#fluxo-de-implementação)
7. [Checklist de Funcionalidades](#checklist-de-funcionalidades)

---

## STACK TECNOLÓGICA

### Core
- **React 18+** - Framework principal
- **Vite** - Build tool
- **TypeScript** - Type safety

### UI & Styling
- **Tailwind CSS v3** - Utility-first CSS framework
- **Lucide React** - Ícones modernos
- **clsx + tailwind-merge** - Concatenação de classes CSS

### State Management
- **Context API** - Gerenciamento de estado do carrinho
- **React Query (TanStack Query)** - Cache e sincronização com API

### HTTP & Data Fetching
- **Axios** - Cliente HTTP
- **React Query** - Cache, refetch automático, loading states

### Development
- **ESLint** - Linting
- **TypeScript** - Type checking

---

## ESTRUTURA DE DIRETÓRIOS

```
frontend/
├── public/
│   └── vite.svg
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Loading.tsx
│   │   │   └── ErrorMessage.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Layout.tsx
│   │   ├── cardapio/
│   │   │   ├── CategoriaNav.tsx
│   │   │   ├── ProdutoCard.tsx
│   │   │   ├── ProdutoModal.tsx
│   │   │   └── IngredientesList.tsx
│   │   └── carrinho/
│   │       ├── CarrinhoSidebar.tsx
│   │       └── CarrinhoItem.tsx
│   ├── contexts/
│   │   └── CarrinhoContext.tsx
│   ├── hooks/
│   │   └── useCardapio.ts
│   ├── pages/
│   │   └── Cardapio.tsx
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── cardapio.types.ts
│   ├── lib/
│   │   └── utils.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── .env.development
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
└── tsconfig.json
```

---

## COMPONENTES PRINCIPAIS

### 1. Header (Layout)
- Logo da pizzaria
- Badge de itens no carrinho
- Botão de busca

### 2. CategoriaNav (Navegação)
- Tabs horizontais com categorias
- Scroll horizontal suave
- Destaque da categoria ativa
- Ícones + nomes das categorias

### 3. ProdutoCard (Lista de Produtos)
- Imagem do produto
- Nome e descrição
- Badge de disponibilidade
- Preços das variações
- Botão "Ver detalhes"
- Hover effect

### 4. ProdutoModal (Detalhes e Customização)
- Imagem do produto
- Nome e descrição completa
- Seletor de variação (tamanho com radio buttons)
- Lista de ingredientes padrão (obrigatórios e opcionais)
- Ingredientes adicionais disponíveis
- Campo de observações (textarea)
- Seletor de quantidade (+ e -)
- Resumo do preço:
  - Preço base
  - Ingredientes adicionados
  - Ingredientes removidos
  - Subtotal com quantidade
- Botões: "Adicionar ao carrinho" e "Cancelar"

### 5. CarrinhoSidebar (Carrinho de Compras)
- Drawer/Sidebar lateral direita
- Lista de itens com:
  - Nome do produto + tamanho
  - Customizações (resumo)
  - Quantidade (+ e -)
  - Preço unitário e total
  - Botão remover
- Resumo:
  - Subtotal
  - Total
- Botão "Finalizar pedido"
- Botão "Continuar comprando"

### 6. SearchBar (Busca)
- Input de busca com ícone
- Debounce de 300ms
- Sugestões em tempo real (dropdown)
- Destaque do termo buscado
- Mínimo 2 caracteres

---

## GERENCIAMENTO DE ESTADO

### Context API - CarrinhoContext

```typescript
interface ItemCarrinho {
  produto: Produto
  variacao: ProdutoVariacao
  quantidade: number
  ingredientesAdicionados: Ingrediente[]
  ingredientesRemovidos: number[]
  observacoes?: string
  preco_total: number
}

interface CarrinhoContextType {
  itens: ItemCarrinho[]
  adicionarItem: (item: ItemCarrinho) => void
  removerItem: (id: string) => void
  atualizarQuantidade: (id: string, quantidade: number) => void
  limparCarrinho: () => void
  totalItens: number
  subtotal: number
}
```

### React Query - Cache de Dados

```typescript
// Queries configuradas:
- useCardapio() - GET /cardapio/
  - Cache: 5 minutos
  - Refetch on window focus: true

- useProdutosPorCategoria(categoriaId) - GET /cardapio/categorias/{id}/produtos
  - Cache: 5 minutos

- useBuscaProdutos(termo) - GET /cardapio/buscar?termo=...
  - Cache: 2 minutos
  - Enabled: termo.length >= 2
```

---

## INTEGRAÇÃO COM API

### Configuração do Axios

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
```

### API Service

```typescript
// src/services/api.ts
export const cardapioApi = {
  getCardapioCompleto: async (): Promise<CardapioResponse> => {
    const response = await api.get<CardapioResponse>('/cardapio/')
    return response.data
  },

  getProdutosPorCategoria: async (
    categoriaId: number,
    incluirIndisponiveis = false
  ): Promise<Produto[]> => {
    const response = await api.get<Produto[]>(
      `/cardapio/categorias/${categoriaId}/produtos`,
      { params: { incluir_indisponiveis: incluirIndisponiveis } }
    )
    return response.data
  },

  buscarProdutos: async (termo: string): Promise<Produto[]> => {
    const response = await api.get<Produto[]>('/cardapio/buscar', {
      params: { termo },
    })
    return response.data
  },
}
```

---

## FLUXO DE IMPLEMENTAÇÃO

### SPRINT 1: Setup e Fundação [CONCLUÍDO - 13/12/2025]

#### Etapa 1.1: Configurar Projeto
- [x] Criar projeto Vite + React + TypeScript
- [x] Configurar Tailwind CSS v3
- [x] Instalar dependências (axios, react-query, lucide-react, clsx, tailwind-merge)
- [x] Configurar ESLint (gerado pelo Vite)
- [x] Criar estrutura de pastas

**Arquivos criados:**
- `frontend/vite.config.ts` - Configuração com path aliases (@/) e proxy para API
- `frontend/tailwind.config.js` - Cores customizadas (primary, secondary, accent)
- `frontend/postcss.config.js` - Configuração PostCSS + Autoprefixer
- `frontend/tsconfig.app.json` - Path aliases TypeScript
- `frontend/.env.development` - VITE_API_URL=http://localhost:8000

#### Etapa 1.2: Setup de API e Types
- [x] Criar arquivo `api.ts` com configuração axios
- [x] Criar funções de API (getCardapioCompleto, getProdutosPorCategoria, buscarProdutos)
- [x] Definir tipos TypeScript em `cardapio.types.ts`
- [x] Configurar React Query em main.tsx (staleTime: 5min, retry: 1)

**Arquivos criados:**
- `frontend/src/services/api.ts` - Cliente Axios + 3 endpoints do cardápio
- `frontend/src/types/cardapio.types.ts` - Interfaces completas do backend
- `frontend/src/lib/utils.ts` - Funções utilitárias (cn, formatarPreco)
- `frontend/src/main.tsx` - QueryClientProvider configurado

**Estrutura de diretórios criada:**
```
src/
├── components/
│   ├── layout/      [pronto para Sprint 2]
│   ├── common/      [pronto para Sprint 2]
│   ├── cardapio/    [pronto para Sprint 3]
│   └── carrinho/    [pronto para Sprint 5]
├── contexts/        [pronto para Sprint 2]
├── hooks/           [pronto para Sprint 3]
├── pages/           [pronto para Sprint 3]
├── services/        [api.ts criado]
├── types/           [cardapio.types.ts criado]
└── lib/             [utils.ts criado]
```

**Status do Sprint 1:**
- Build funcionando (npm run build executado com sucesso)
- Servidor de desenvolvimento rodando em http://localhost:5173/
- TypeScript sem erros
- Tailwind CSS v3 configurado
- Proxy para API configurado
- React Query configurado

---

### SPRINT 2: Layout e Navegação [EM PROGRESSO]

#### Etapa 2.1: Componentes Base [CONCLUÍDO - 16/12/2025]
- [x] Criar componente `Button`
- [x] Criar componente `Card`
- [x] Criar componente `Badge`
- [x] Criar componente `Loading` (spinner)
- [x] Criar componente `ErrorMessage`

**Arquivos criados:**
- `frontend/src/components/common/Button.tsx` - 5 variantes, 3 tamanhos, loading state
- `frontend/src/components/common/Badge.tsx` - 5 cores, 3 tamanhos, dot indicator
- `frontend/src/components/common/Card.tsx` - 3 variantes, hover effects
- `frontend/src/components/common/Loading.tsx` - 3 animações, fullScreen mode
- `frontend/src/components/common/ErrorMessage.tsx` - 3 layouts, retry action
- `frontend/src/App.tsx` - Página de testes com todos os componentes

**Validações:**
- ✅ TypeScript sem erros
- ✅ Build production: 258.31 kB (79.92 kB gzip)
- ✅ Todos os componentes com forwardRef e tipos
- ✅ Acessibilidade (focus, aria, keyboard)

#### Etapa 2.2: Layout Principal [CONCLUÍDO - 16/12/2025]
- [x] Criar `Header` com logo e badge de carrinho
- [x] Criar `Footer` básico
- [x] Criar `Layout` wrapper

**Arquivos criados:**
- `frontend/src/components/layout/Header.tsx` - Header fixo com logo (Pizza icon), carrinho com badge
- `frontend/src/components/layout/Footer.tsx` - Footer simples com copyright e créditos
- `frontend/src/components/layout/Layout.tsx` - Wrapper que combina Header + conteúdo + Footer
- `frontend/src/App.tsx` - Atualizado para usar Layout e testar todos os componentes

**Features:**
- ✅ Header sticky (position: sticky, top: 0)
- ✅ Badge de carrinho com contador (máx 99+)
- ✅ Logo clicável (Pizza icon + texto)
- ✅ Footer com copyright dinâmico (ano atual)
- ✅ Layout responsivo (mobile first)
- ✅ Max-width configurável (full, 7xl, 6xl, 5xl)
- ✅ Padding opcional (noPadding prop)

**Validações:**
- ✅ TypeScript sem erros
- ✅ Build production: 261.96 kB (81.04 kB gzip)
- ✅ Teste de scroll (Header permanece fixo)
- ✅ Props tipadas com interfaces

#### Etapa 2.3: Context do Carrinho [CONCLUÍDO - 17/12/2025]
- [x] Criar `CarrinhoContext` com estado inicial
- [x] Implementar funções de adicionar/remover/atualizar
- [x] Persistir carrinho no localStorage
- [x] Criar hook `useCarrinho`

**Arquivos criados:**
- `frontend/src/contexts/CarrinhoContext.tsx` - Context API completo com todas as operações do carrinho
- `frontend/src/App.tsx` - Atualizado para integrar CarrinhoProvider e testar funcionalidades
- `frontend/src/components/layout/Footer.tsx` - Atualizado (removido créditos)

**Features:**
- ✅ Interface ItemCarrinho com cálculo automático de preço total
- ✅ adicionarItem() - Adiciona item com ingredientes e calcula preço (base + adicionais × quantidade)
- ✅ removerItem(id) - Remove item específico do carrinho
- ✅ atualizarQuantidade(id, qtd) - Atualiza quantidade e recalcula preço automaticamente
- ✅ limparCarrinho() - Remove todos os itens
- ✅ Computed values: totalItens (soma de quantidades), subtotal (soma de preços)
- ✅ Persistência bidirecional em localStorage (carrega ao iniciar, salva a cada mudança)
- ✅ Hook useCarrinho() com validação automática
- ✅ Tratamento de erros no localStorage (try/catch)
- ✅ IDs únicos gerados com crypto.randomUUID()
- ✅ Seção de testes interativa no App.tsx

**Validações:**
- ✅ TypeScript sem erros
- ✅ Build production: 266.38 kB (82.41 kB gzip)
- ✅ Todas as operações testadas e funcionando
- ✅ Badge do Header atualiza automaticamente com totalItens
- ✅ localStorage persiste dados entre reloads

#### Etapa 2.4: Navegação de Categorias [CONCLUÍDO - 17/12/2025]
- [x] Criar `CategoriaNav` com tabs
- [x] Implementar scroll horizontal suave
- [x] Adicionar indicador de categoria ativa
- [x] Testar com dados reais da API

**Arquivos criados:**
- `frontend/src/hooks/useCardapio.ts` - Hooks React Query para buscar dados da API
- `frontend/src/components/cardapio/CategoriaNav.tsx` - Componente de navegação por categorias
- `frontend/src/index.css` - Atualizado com classe .scrollbar-hide
- `frontend/src/App.tsx` - Atualizado para integrar CategoriaNav e testar funcionalidades

**Features:**
- ✅ **Hooks especializados:**
  - useCardapio() - Busca cardápio completo (GET /cardapio/)
  - useProdutosPorCategoria(id) - Filtra produtos por categoria
  - useBuscaProdutos(termo) - Busca produtos por termo
  - React Query com cache de 5 minutos e refetch automático
- ✅ **CategoriaNav Component:**
  - Tabs horizontais com scroll suave (scrollbar oculta)
  - Ícones dinâmicos por categoria (Pizza, Coffee, Wine, IceCream, etc)
  - Mapeamento automático de ícones baseado no nome da categoria
  - Indicador visual de categoria ativa (bg-primary-600, texto branco)
  - Auto-scroll para centralizar categoria selecionada (useEffect + useRef)
  - Badge com contador de produtos por categoria
  - Animação de pulse no ícone da categoria ativa
  - Gradiente visual indicando scroll disponível
  - Estados hover, focus e active (acessibilidade)
  - Ordenação por ordem_exibicao
  - Filtro de categorias ativas
- ✅ **Integração com API:**
  - Conexão com backend via React Query
  - Fallback para dados mockados caso API esteja offline
  - Loading states e error handling
  - Seção de testes interativa no App.tsx

**Validações:**
- ✅ TypeScript sem erros
- ✅ Build production: 318.30 kB (102.25 kB gzip)
- ✅ HMR funcionando perfeitamente
- ✅ Scroll horizontal suave e responsivo
- ✅ Componente totalmente reutilizável
- ✅ Props tipadas com TypeScript
- ✅ Acessibilidade (keyboard navigation, focus states)

---

### SPRINT 3: Listagem de Produtos

#### Etapa 3.1: Hook de Cardápio [CONCLUÍDO - 17/12/2025]
- [x] Criar `useCardapio` com React Query
- [x] Implementar cache e refetch automático
- [x] Adicionar loading e error states

**Nota:** Esta etapa foi implementada junto com a Etapa 2.4. Ver detalhes em `frontend/src/hooks/useCardapio.ts`.

#### Etapa 3.2: Cards de Produtos [CONCLUÍDO - 26/12/2025]
- [x] Criar `ProdutoCard` com layout responsivo
- [x] Adicionar imagem, nome, descrição
- [x] Mostrar faixa de preços (variações)
- [x] Implementar hover effects
- [x] Grid responsivo

**Arquivos criados:**
- `frontend/src/components/cardapio/ProdutoCard.tsx` - Componente de card de produto completo
- `frontend/src/TestProdutoCard.tsx` - Arquivo de teste temporário (6 cenários diferentes)

**Features:**
- ✅ **Layout responsivo** - Card com aspect ratio 4:3 para imagens
- ✅ **Imagem com lazy loading** - Carregamento otimizado de imagens
- ✅ **Placeholder automático** - Imagem gerada quando produto não tem imagem
- ✅ **Badges de status:**
  - Produto indisponível (overlay com badge "Indisponível")
  - Sem variações (badge de aviso)
  - Customizável (badge quando tem ingredientes)
  - Contador de tamanhos disponíveis
- ✅ **Faixa de preços inteligente:**
  - "A partir de R$ X até R$ Y" (múltiplas variações)
  - Preço único quando todas variações têm mesmo valor
  - "Consulte disponibilidade" para produtos sem variações
- ✅ **Hover effects:**
  - Elevação do card (shadow-md + translate)
  - Escala da imagem (scale-105)
  - Transições suaves (duration-300)
- ✅ **Line-clamp** - Limita nome e descrição a 2 linhas
- ✅ **Botão de ação** - "Ver detalhes" (disabled se indisponível)
- ✅ **Formatação de preço** - Valores em Real (R$) usando Intl.NumberFormat
- ✅ **Reutilização de componentes** - Usa Card, Badge e Button já criados
- ✅ **TypeScript** - Totalmente tipado com forwardRef

**Validações:**
- ✅ TypeScript sem erros
- ✅ Build production: 258.86 kB (81.05 kB gzip)
- ✅ Grid responsivo (1 col mobile → 2 tablet → 3 desktop → 4 xl)
- ✅ 6 cenários testados (disponível, indisponível, sem imagem, sem descrição, etc)
- ✅ Props tipadas e documentadas
- ✅ Componente reutilizável e extensível

#### Etapa 3.3: Página de Cardápio
- [ ] Criar página `Cardapio.tsx`
- [ ] Integrar `CategoriaNav` + grid de produtos
- [ ] Filtrar produtos por categoria selecionada
- [ ] Implementar scroll suave ao trocar categoria

---

### SPRINT 4: Modal de Customização

#### Etapa 4.1: Modal Base
- [ ] Criar componente `Modal` genérico
- [ ] Implementar overlay e animações
- [ ] Adicionar botão de fechar (ESC + click fora)

#### Etapa 4.2: Seletor de Variação
- [ ] Criar seletor com radio buttons
- [ ] Mostrar tamanho e preço de cada variação
- [ ] Atualizar preço base ao selecionar

#### Etapa 4.3: Customização de Ingredientes
- [ ] Criar lista de ingredientes
- [ ] Listar ingredientes padrão (disabled se obrigatório)
- [ ] Listar ingredientes adicionais disponíveis
- [ ] Calcular preço de ingredientes em tempo real
- [ ] Adicionar campo de observações

#### Etapa 4.4: Resumo e Adicionar ao Carrinho
- [ ] Criar seletor de quantidade (+ e -)
- [ ] Calcular preço total (base + ingredientes x quantidade)
- [ ] Implementar botão "Adicionar ao carrinho"
- [ ] Mostrar feedback de sucesso

---

### SPRINT 5: Carrinho de Compras

#### Etapa 5.1: Sidebar do Carrinho
- [ ] Criar `CarrinhoSidebar` (drawer lateral)
- [ ] Implementar toggle (abrir/fechar)
- [ ] Animação de slide-in/out

#### Etapa 5.2: Item do Carrinho
- [ ] Criar `CarrinhoItem` com layout compacto
- [ ] Mostrar nome, tamanho, customizações
- [ ] Seletor de quantidade inline (+ e -)
- [ ] Botão remover item
- [ ] Atualizar preço ao alterar quantidade

#### Etapa 5.3: Resumo do Carrinho
- [ ] Criar resumo com cálculos
- [ ] Mostrar subtotal
- [ ] Botão "Finalizar pedido" (disabled se vazio)
- [ ] Botão "Continuar comprando"

#### Etapa 5.4: Badge do Carrinho
- [ ] Criar badge no header
- [ ] Mostrar número de itens
- [ ] Animação ao adicionar item

---

### SPRINT 6: Busca e Refinamentos

#### Etapa 6.1: Barra de Busca
- [ ] Criar `SearchBar` com debounce
- [ ] Implementar `useBuscaProdutos` hook
- [ ] Mostrar resultados em dropdown
- [ ] Destacar termo buscado

#### Etapa 6.2: Estados de Loading e Erro
- [ ] Adicionar skeletons de loading
- [ ] Criar mensagens de erro amigáveis
- [ ] Implementar retry em caso de falha
- [ ] Adicionar estado vazio ("Nenhum produto encontrado")

#### Etapa 6.3: Responsividade
- [ ] Testar em mobile (320px+)
- [ ] Testar em tablet (768px+)
- [ ] Testar em desktop (1024px+)
- [ ] Ajustar modal para mobile

---

### SPRINT 7: Polimento e Testes

#### Etapa 7.1: UX/UI Refinements
- [ ] Adicionar transições suaves
- [ ] Melhorar feedback visual (hover, focus, active)
- [ ] Adicionar tooltips informativos
- [ ] Otimizar imagens (lazy loading)

#### Etapa 7.2: Acessibilidade
- [ ] Navegação por teclado
- [ ] ARIA labels
- [ ] Contraste de cores (WCAG AA)
- [ ] Focus visible

#### Etapa 7.3: Performance
- [ ] Code splitting
- [ ] Lazy loading de componentes
- [ ] Otimizar bundle size
- [ ] Lighthouse audit (objetivo: 90+)

#### Etapa 7.4: Testes
- [ ] Testes unitários de componentes críticos
- [ ] Testes de integração do carrinho
- [ ] Testes de API (mock)

---

## CHECKLIST DE FUNCIONALIDADES

### Visualização de Cardápio
- [ ] Listagem de categorias ordenada
- [ ] Grid responsivo de produtos
- [ ] Filtro por categoria
- [ ] Busca de produtos (mínimo 2 caracteres)
- [ ] Destaque de produtos indisponíveis
- [ ] Lazy loading de imagens

### Customização de Produtos
- [ ] Modal de detalhes do produto
- [ ] Seleção de variação (tamanho/preço)
- [ ] Ingredientes padrão (obrigatórios e opcionais)
- [ ] Ingredientes adicionais
- [ ] Campo de observações
- [ ] Seletor de quantidade
- [ ] Cálculo de preço em tempo real
- [ ] Validação antes de adicionar ao carrinho

### Carrinho de Compras
- [ ] Sidebar lateral responsiva
- [ ] Adicionar item ao carrinho
- [ ] Remover item do carrinho
- [ ] Atualizar quantidade (+ e -)
- [ ] Persistência no localStorage
- [ ] Badge com número de itens
- [ ] Cálculo de subtotal
- [ ] Carrinho vazio (mensagem amigável)
- [ ] Limpar carrinho

### UX/UI
- [ ] Loading states (skeletons)
- [ ] Error states (mensagens amigáveis)
- [ ] Feedback de ações
- [ ] Responsividade completa
- [ ] Transições suaves
- [ ] Acessibilidade (teclado, ARIA)

### Integração
- [ ] Conexão com API FastAPI
- [ ] Cache de dados (React Query)
- [ ] Tratamento de erros de rede
- [ ] CORS configurado
- [ ] Variáveis de ambiente (.env)

---

## METAS DE QUALIDADE

### Performance
- First Contentful Paint < 1.5s
- Time to Interactive < 3s
- Lighthouse Score > 90
- Bundle size < 500kb

### Acessibilidade
- WCAG 2.1 AA compliance
- Navegação completa por teclado
- Screen reader friendly
- Contraste mínimo 4.5:1

### Responsividade
- Mobile First (320px+)
- Tablet (768px+)
- Desktop (1024px+)
- Large Desktop (1440px+)

---

## VARIÁVEIS DE AMBIENTE

```bash
# .env.development
VITE_API_URL=http://localhost:8000
```

---

## STATUS ATUAL E PRÓXIMOS PASSOS

### Concluído

**Sprint 1: Setup e Fundação** - 100% completo (13/12/2025)
- Projeto Vite + React + TypeScript configurado
- Tailwind CSS v3 instalado
- API service e tipos TypeScript criados
- React Query configurado
- Estrutura de diretórios pronta

**Sprint 2: Layout e Navegação** - 100% completo (17/12/2025)
- ✅ Etapa 2.1: Componentes Base (Button, Badge, Card, Loading, ErrorMessage)
- ✅ Etapa 2.2: Layout Principal (Header, Footer, Layout)
- ✅ Etapa 2.3: Context do Carrinho (CarrinhoContext + useCarrinho hook)
- ✅ Etapa 2.4: Navegação de Categorias (CategoriaNav + useCardapio hook)

**Sprint 3: Listagem de Produtos** - 67% completo (26/12/2025)
- ✅ Etapa 3.1: Hook de Cardápio (useCardapio, useProdutosPorCategoria, useBuscaProdutos)
- ✅ Etapa 3.2: Cards de Produtos (ProdutoCard.tsx + TestProdutoCard.tsx)
- ⏳ Etapa 3.3: Página de Cardápio (pendente)

### Próximo Passo: Sprint 3 - Etapa 3.3 (Página de Cardápio)

**Para continuar:**

1. Servidor já rodando em: http://localhost:5173/

2. **Tarefas da Etapa 3.3 - Página de Cardápio:**
   - Criar `src/pages/Cardapio.tsx`
     - Integrar CategoriaNav no topo
     - Grid de produtos usando ProdutoCard
     - Filtrar produtos por categoria selecionada
     - Estados de loading, erro e lista vazia
     - Scroll suave ao trocar categoria
   - Atualizar App.tsx para usar a página Cardapio
   - Testar integração completa com dados da API

**Arquivos importantes criados:**
- `frontend/src/services/api.ts` - API do cardápio (3 endpoints)
- `frontend/src/types/cardapio.types.ts` - Tipos TypeScript completos
- `frontend/src/lib/utils.ts` - Funções utilitárias (cn, formatarPreco)
- `frontend/src/contexts/CarrinhoContext.tsx` - Context do carrinho + useCarrinho hook
- `frontend/src/hooks/useCardapio.ts` - Hooks React Query (3 hooks)
- `frontend/src/components/layout/` - Header, Footer, Layout
- `frontend/src/components/common/` - Button, Badge, Card, Loading, ErrorMessage
- `frontend/src/components/cardapio/` - CategoriaNav, ProdutoCard

**Comandos úteis:**
```bash
# Verificar build
npm run build

# Verificar TypeScript
npx tsc --noEmit

# Servidor dev
npm run dev
```
