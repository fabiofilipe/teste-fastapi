#  PLANO DE IMPLEMENTAÇÃO - FRONTEND DO CARDÁPIO

**Data:** 13/12/2025
**Fase:** 1.3 - Sistema de Categorias e Cardápio Dinâmico
**Objetivo:** Criar interface completa de visualização e compra de produtos

---

##  ÍNDICE

1. [Stack Tecnológica](#stack-tecnológica)
2. [Estrutura de Diretórios](#estrutura-de-diretórios)
3. [Componentes Principais](#componentes-principais)
4. [Gerenciamento de Estado](#gerenciamento-de-estado)
5. [Integração com API](#integração-com-api)
6. [Fluxo de Implementação](#fluxo-de-implementação)
7. [Checklist de Funcionalidades](#checklist-de-funcionalidades)

---

##  STACK TECNOLÓGICA

### Core
- **React 18+** - Framework principal
- **Vite** - Build tool (mais rápido que CRA)
- **TypeScript** - Type safety 

### UI & Styling
- **Tailwind CSS** - Utility-first CSS framework
- **Headless UI** ou **Radix UI** - Componentes acessíveis
- **Lucide React** - Ícones modernos
- **Framer Motion** - Animações suaves

### State Management
- **Context API** - Gerenciamento de estado do carrinho
- **React Query (TanStack Query)** - Cache e sincronização com API
- **Zustand** - Estado global leve (alternativa ao Context)

### HTTP & Data Fetching
- **Axios** - Cliente HTTP
- **React Query** - Cache, refetch automático, loading states

### Utilities
- **React Hook Form** - Formulários (para checkout futuro)
- **Zod** - Validação de dados
- **clsx** ou **classnames** - Concatenação de classes CSS
- **date-fns** - Manipulação de datas

### Development
- **ESLint** - Linting
- **Prettier** - Formatação de código
- **Vitest** - Testes unitários (compatível com Vite)
- **React Testing Library** - Testes de componentes

---

##  ESTRUTURA DE DIRETÓRIOS

```
frontend/
├── public/
│   ├── images/
│   │   ├── products/          # Imagens de produtos
│   │   ├── categories/        # Ícones de categorias
│   │   └── placeholder.png    # Imagem padrão
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── common/            # Componentes reutilizáveis
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Loading.tsx
│   │   │   └── ErrorMessage.tsx
│   │   ├── layout/            # Layout da aplicação
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── MainLayout.tsx
│   │   ├── cardapio/          # Componentes específicos do cardápio
│   │   │   ├── CategoriaNav.tsx
│   │   │   ├── ProdutoCard.tsx
│   │   │   ├── ProdutoModal.tsx
│   │   │   ├── VariacaoSelector.tsx
│   │   │   ├── IngredientesCheckbox.tsx
│   │   │   └── SearchBar.tsx
│   │   └── carrinho/          # Componentes do carrinho
│   │       ├── CarrinhoSidebar.tsx
│   │       ├── CarrinhoItem.tsx
│   │       ├── CarrinhoResumo.tsx
│   │       └── CarrinhoBadge.tsx
│   ├── contexts/
│   │   └── CarrinhoContext.tsx
│   ├── hooks/
│   │   ├── useCardapio.ts
│   │   ├── useCarrinho.ts
│   │   └── useBusca.ts
│   ├── services/
│   │   ├── api.ts             # Configuração axios
│   │   └── cardapioService.ts # Endpoints do cardápio
│   ├── types/
│   │   └── cardapio.types.ts  # Tipos TypeScript
│   ├── utils/
│   │   ├── formatters.ts      # Formatação de moeda, etc.
│   │   └── validators.ts      # Validações
│   ├── pages/
│   │   ├── Cardapio.tsx       # Página principal
│   │   └── NotFound.tsx       # 404
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── .env.development
├── .env.production
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── README.md
```

---

## COMPONENTES PRINCIPAIS

### 1. **Header** (Layout)
```tsx
- Logo da pizzaria
- Badge de itens no carrinho (ex: 🛒 3)
- Botão de busca
- (Futuro) Login/Perfil
```

### 2. **CategoriaNav** (Navegação)
```tsx
- Tabs horizontais com categorias
- Scroll horizontal suave
- Destaque da categoria ativa
- Ícones + nomes das categorias
- Contagem de produtos por categoria
```

### 3. **ProdutoCard** (Lista de Produtos)
```tsx
- Imagem do produto
- Nome e descrição
- Badge de disponibilidade
- Preços das variações (a partir de R$ X,XX)
- Botão "Ver detalhes"
- Hover effect
```

### 4. **ProdutoModal** (Detalhes e Customização)
```tsx
- Imagem maior do produto
- Nome e descrição completa
- Seletor de variação (tamanho):
  - Radio buttons (Pequena, Média, Grande, Gigante)
  - Preço de cada variação
- Lista de ingredientes padrão:
  - Ingredientes obrigatórios (checkbox disabled + tooltip)
  - Ingredientes opcionais (checkbox)
  - Preço adicional (se houver)
- Ingredientes adicionais disponíveis:
  - Checkboxes de ingredientes extras
  - Preço de cada um
- Campo de observações (textarea)
- Seletor de quantidade (+ e -)
- Resumo do preço:
  - Preço base: R$ X,XX
  - Ingredientes adicionados: R$ Y,YY
  - Ingredientes removidos: -R$ Z,ZZ
  - Subtotal: R$ TOTAL × quantidade
- Botões:
  - "Adicionar ao carrinho" (primary)
  - "Cancelar" (secondary)
```

### 5. **CarrinhoSidebar** (Carrinho de Compras)
```tsx
- Drawer/Sidebar lateral direita
- Lista de itens:
  - Nome do produto + tamanho
  - Customizações (resumo)
  - Quantidade (+ e -)
  - Preço unitário e total
  - Botão remover (🗑️)
- Resumo:
  - Subtotal
  - (Futuro) Taxa de entrega
  - Total
- Botão "Finalizar pedido" (disabled se carrinho vazio)
- Botão "Continuar comprando"
```

### 6. **SearchBar** (Busca)
```tsx
- Input de busca com ícone 🔍
- Debounce de 300ms
- Sugestões em tempo real (dropdown)
- Destaque do termo buscado
- Mínimo 2 caracteres
```

---

## GERENCIAMENTO DE ESTADO

### Context API - CarrinhoContext

```typescript
interface ItemCarrinho {
  id: string; // Gerado localmente (UUID)
  produtoId: number;
  produtoNome: string;
  variacaoId: number;
  tamanho: string;
  precoBase: number;
  quantidade: number;
  ingredientesAdicionados: { id: number; nome: string; preco: number }[];
  ingredientesRemovidos: number[];
  observacoes?: string;
  precoTotal: number;
}

interface CarrinhoContextType {
  itens: ItemCarrinho[];
  adicionarItem: (item: ItemCarrinho) => void;
  removerItem: (id: string) => void;
  atualizarQuantidade: (id: string, quantidade: number) => void;
  limparCarrinho: () => void;
  totalItens: number;
  subtotal: number;
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

## 🔌 INTEGRAÇÃO COM API

### Configuração do Axios

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptors para logging e tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Tratamento global de erros
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default api;
```

### Service Layer

```typescript
// src/services/cardapioService.ts
import api from './api';
import { CardapioResponse, ProdutoResponse } from '@/types';

export const cardapioService = {
  async getCardapioCompleto(): Promise<CardapioResponse> {
    const { data } = await api.get('/cardapio/');
    return data;
  },

  async getProdutosPorCategoria(
    categoriaId: number,
    incluirIndisponiveis = false
  ): Promise<ProdutoResponse[]> {
    const { data } = await api.get(
      `/cardapio/categorias/${categoriaId}/produtos`,
      { params: { incluir_indisponiveis: incluirIndisponiveis } }
    );
    return data;
  },

  async buscarProdutos(termo: string): Promise<ProdutoResponse[]> {
    const { data } = await api.get('/cardapio/buscar', {
      params: { termo },
    });
    return data;
  },
};
```

---

## FLUXO DE IMPLEMENTAÇÃO

### **SPRINT 1: Setup e Fundação** (1-2 dias)

#### Etapa 1.1: Configurar Projeto
- [ ] Criar projeto Vite + React + TypeScript
- [ ] Configurar Tailwind CSS
- [ ] Instalar dependências (axios, react-query, lucide-react, etc.)
- [ ] Configurar ESLint e Prettier
- [ ] Criar estrutura de pastas

#### Etapa 1.2: Setup de API e Types
- [ ] Criar arquivo `api.ts` com configuração axios
- [ ] Criar `cardapioService.ts` com endpoints
- [ ] Definir tipos TypeScript em `cardapio.types.ts`
- [ ] Testar conexão com backend (verificar CORS)

#### Etapa 1.3: Componentes Base
- [ ] Criar componente `Button`
- [ ] Criar componente `Card`
- [ ] Criar componente `Badge`
- [ ] Criar componente `Loading` (spinner)
- [ ] Criar componente `ErrorMessage`

---

### **SPRINT 2: Layout e Navegação** (1-2 dias)

#### Etapa 2.1: Layout Principal
- [ ] Criar `Header` com logo e badge de carrinho
- [ ] Criar `Footer` básico
- [ ] Criar `MainLayout` wrapper

#### Etapa 2.2: Context do Carrinho
- [ ] Criar `CarrinhoContext` com estado inicial
- [ ] Implementar funções de adicionar/remover/atualizar
- [ ] Persistir carrinho no localStorage
- [ ] Criar hook `useCarrinho`

#### Etapa 2.3: Navegação de Categorias
- [ ] Criar `CategoriaNav` com tabs
- [ ] Implementar scroll horizontal suave
- [ ] Adicionar indicador de categoria ativa
- [ ] Testar com dados reais da API

---

### **SPRINT 3: Listagem de Produtos** (2-3 dias)

#### Etapa 3.1: Hook de Cardápio
- [ ] Criar `useCardapio` com React Query
- [ ] Implementar cache e refetch automático
- [ ] Adicionar loading e error states

#### Etapa 3.2: Cards de Produtos
- [ ] Criar `ProdutoCard` com layout responsivo
- [ ] Adicionar imagem, nome, descrição
- [ ] Mostrar faixa de preços (variações)
- [ ] Implementar hover effects
- [ ] Grid responsivo (1 col mobile, 2-3 cols tablet, 3-4 cols desktop)

#### Etapa 3.3: Página de Cardápio
- [ ] Criar página `Cardapio.tsx`
- [ ] Integrar `CategoriaNav` + grid de produtos
- [ ] Filtrar produtos por categoria selecionada
- [ ] Implementar scroll suave ao trocar categoria

---

### **SPRINT 4: Modal de Customização** (2-3 dias)

#### Etapa 4.1: Modal Base
- [ ] Criar componente `Modal` genérico
- [ ] Implementar overlay e animações
- [ ] Adicionar botão de fechar (ESC + click fora)

#### Etapa 4.2: Seletor de Variação
- [ ] Criar `VariacaoSelector` com radio buttons
- [ ] Mostrar tamanho e preço de cada variação
- [ ] Atualizar preço base ao selecionar

#### Etapa 4.3: Customização de Ingredientes
- [ ] Criar `IngredientesCheckbox`
- [ ] Listar ingredientes padrão (disabled se obrigatório)
- [ ] Listar ingredientes adicionais disponíveis
- [ ] Calcular preço de ingredientes em tempo real
- [ ] Adicionar campo de observações

#### Etapa 4.4: Resumo e Adicionar ao Carrinho
- [ ] Criar seletor de quantidade (+ e -)
- [ ] Calcular preço total (base + ingredientes × quantidade)
- [ ] Implementar botão "Adicionar ao carrinho"
- [ ] Mostrar feedback de sucesso (toast ou animação)

---

### **SPRINT 5: Carrinho de Compras** (2 dias)

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
- [ ] Criar `CarrinhoResumo` com cálculos
- [ ] Mostrar subtotal
- [ ] Botão "Finalizar pedido" (disabled se vazio)
- [ ] Botão "Continuar comprando"

#### Etapa 5.4: Badge do Carrinho
- [ ] Criar `CarrinhoBadge` no header
- [ ] Mostrar número de itens
- [ ] Animação ao adicionar item

---

### **SPRINT 6: Busca e Refinamentos** (1-2 dias)

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

### **SPRINT 7: Polimento e Testes** (1-2 dias)

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
- [ ] Feedback de ações (toasts/animações)
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
-  First Contentful Paint < 1.5s
-  Time to Interactive < 3s
-  Lighthouse Score > 90
-  Bundle size < 500kb

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

##  VARIÁVEIS DE AMBIENTE

```bash
# .env.development
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Pizzaria XYZ
VITE_ENABLE_ANALYTICS=false

# .env.production
VITE_API_URL=https://api.pizzaria.com
VITE_APP_NAME=Pizzaria XYZ
VITE_ENABLE_ANALYTICS=true
```

---

## RECURSOS E REFERÊNCIAS

### Design Inspiration
- [iFood Web](https://www.ifood.com.br/)
- [Rappi](https://www.rappi.com.br/)
- [Uber Eats](https://www.ubereats.com/br)
- [Dribbble - Food Ordering](https://dribbble.com/search/food-ordering)

### UI Components
- [Tailwind UI](https://tailwindui.com/)
- [Headless UI](https://headlessui.com/)
- [Radix UI](https://www.radix-ui.com/)
- [shadcn/ui](https://ui.shadcn.com/)

### Icons
- [Lucide Icons](https://lucide.dev/)
- [Heroicons](https://heroicons.com/)

---

## PRÓXIMOS PASSOS

1. **Agora**: Criar projeto Vite + React
2. **Depois**: Implementar componentes base
3. **Em seguida**: Integrar com API
4. **Por fim**: Polir e testar

