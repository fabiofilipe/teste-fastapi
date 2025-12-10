# Backend - Sistema de Pizzaria

API RESTful desenvolvida com FastAPI para gerenciamento de pedidos de pizzaria.

## Funcionalidades

- **Autenticação JWT**: Sistema de login com access tokens e refresh tokens
- **Gerenciamento de Usuários**: Cadastro e autenticação de usuários
- **Sistema de Categorias**: Organização do cardápio em categorias ordenadas
- **Gerenciamento de Ingredientes**: Catálogo de ingredientes com controle de disponibilidade e preços
- **Produtos com Variações**: Produtos flexíveis com múltiplos tamanhos e preços
- **Cardápio Dinâmico**: API pública otimizada para exibição do cardápio
- **Customização de Pedidos**: Adicionar/remover ingredientes com cálculo automático de preços
- **Gerenciamento de Pedidos**: Criação, listagem e atualização de pedidos com histórico completo

## Requisitos

- Python 3.12+
- SQLite (incluído no Python)

## Instalação

1. Criar e ativar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Popular Banco de Dados (Seed Data)

Antes de executar pela primeira vez, popule o banco com dados iniciais:

```bash
python -m app.seed_data
```

Isso criará:
- 3 categorias (Pizzas, Bebidas, Sobremesas)
- 15 ingredientes
- 10 produtos com variações
- 2 usuários (admin e cliente de teste)

**Credenciais de teste:**
- Admin: `admin@pizzaria.com` / `admin123`
- Cliente: `cliente@teste.com` / `senha123`

## Executar o Servidor

```bash
# Modo desenvolvimento (com auto-reload)
uvicorn app.main:app --reload

# Especificar host e porta
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em: `http://localhost:8000`

## Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação FastAPI principal
│   ├── config.py            # Configurações e variáveis de ambiente
│   ├── database.py          # Configuração do banco de dados
│   ├── seed_data.py         # Script para popular banco com dados iniciais
│   ├── exceptions.py        # Exceções customizadas
│   ├── error_handlers.py    # Handlers de erro
│   ├── dependencies/        # Dependências (auth, etc)
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   └── models.py
│   ├── schemas/             # Schemas Pydantic
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── routers/             # Rotas da API
│       ├── __init__.py
│       ├── auth.py          # Autenticação
│       ├── categorias.py    # Categorias do cardápio (admin)
│       ├── ingredientes.py  # Ingredientes (admin)
│       ├── products.py      # Produtos com variações (admin)
│       ├── cardapio.py      # Cardápio público (leitura)
│       ├── orders.py        # Pedidos com customizações
│       └── health.py        # Health check e métricas
├── tests/                   # Testes automatizados
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Endpoints Principais

### Autenticação
- `POST /auth/criar_conta` - Criar nova conta
- `POST /auth/login` - Login (retorna access_token e refresh_token)

### Cardápio (Público)
- `GET /cardapio/` - Cardápio completo com categorias e produtos
- `GET /cardapio/categorias/{id}/produtos` - Produtos de uma categoria
- `GET /cardapio/buscar?termo=` - Buscar produtos por nome/descrição

### Categorias (Admin)
- `POST /categorias/` - Criar categoria
- `GET /categorias/` - Listar categorias
- `PUT /categorias/{id}` - Atualizar categoria
- `DELETE /categorias/{id}` - Deletar categoria

### Ingredientes (Admin)
- `POST /ingredientes/` - Criar ingrediente
- `GET /ingredientes/` - Listar ingredientes
- `PUT /ingredientes/{id}` - Atualizar ingrediente
- `PATCH /ingredientes/{id}/disponibilidade` - Alternar disponibilidade
- `DELETE /ingredientes/{id}` - Deletar ingrediente

### Produtos (Admin)
- `POST /produtos/` - Criar produto com variações
- `GET /produtos/` - Listar produtos
- `GET /produtos/{id}` - Buscar produto
- `PUT /produtos/{id}` - Atualizar produto
- `DELETE /produtos/{id}` - Deletar produto
- `POST /produtos/{id}/variacoes` - Adicionar variação
- `PUT /produtos/{id}/variacoes/{variacao_id}` - Atualizar variação
- `DELETE /produtos/{id}/variacoes/{variacao_id}` - Deletar variação
- `POST /produtos/{id}/ingredientes/{ingrediente_id}` - Adicionar ingrediente padrão
- `DELETE /produtos/{id}/ingredientes/{ingrediente_id}` - Remover ingrediente padrão

### Pedidos
- `GET /pedidos/meus` - Meus pedidos
- `GET /pedidos/meus/estatisticas` - Estatísticas dos meus pedidos
- `GET /pedidos/` - Listar todos os pedidos (admin)
- `GET /pedidos/{id}` - Buscar pedido por ID
- `POST /pedidos/calcular-preco` - Calcular preço antes de criar
- `POST /pedidos/` - Criar novo pedido com customizações
- `PATCH /pedidos/{id}/status` - Atualizar status do pedido (admin)
- `DELETE /pedidos/{id}` - Cancelar pedido

## Modelo de Dados

### Usuário
- id, nome, email, senha (hash), ativo, admin, endereco

### Categoria
- id, nome, descricao, icone, ordem_exibicao, ativa
- Organiza produtos no cardápio

### Ingrediente
- id, nome, preco_adicional, disponivel
- Catálogo master de ingredientes

### Produto
- id, categoria_id, nome, descricao, imagem_url, disponivel
- Produto base (ex: "Pizza Margherita")

### ProdutoVariacao
- id, produto_id, tamanho, preco, disponivel
- Variações de tamanho/preço do produto
- Tamanhos: PEQUENA, MEDIA, GRANDE, GIGANTE, UNICO

### ProdutoIngrediente (Associação)
- id, produto_id, ingrediente_id, quantidade, obrigatorio
- Ingredientes padrão de cada produto

### Pedido
- id, status, usuario_id, endereco_entrega_id, preco_total
- Status: PENDENTE, EM_PREPARO, PRONTO, ENTREGUE, CANCELADO

### ItemPedido
- id, pedido_id, produto_variacao_id, quantidade
- **Snapshot**: produto_nome, tamanho, preco_base (histórico)
- **Customizações**: ingredientes_adicionados, ingredientes_removidos (JSON)
- preco_ingredientes, preco_total, observacoes

## Breaking Changes (v2.0)

⚠️ **Atenção**: Esta versão introduz mudanças disruptivas na estrutura de dados.

### Banco de Dados
- **Banco limpo necessário**: Delete o arquivo `banco.db` antes de executar
- As tabelas serão recriadas automaticamente com a nova estrutura

### Mudanças nos Modelos
1. **Produto**:
   - ❌ Removido: `categoria` (string), `tamanho`, `preco`
   - ✅ Adicionado: `categoria_id` (FK), `imagem_url`
   - Produtos agora têm múltiplas variações de tamanho/preço

2. **ItemPedido**:
   - ❌ Removido: `produto_id`, `sabor`, `preco_unitario`
   - ✅ Adicionado: `produto_variacao_id`, `produto_nome`, `preco_base`, `ingredientes_adicionados`, `ingredientes_removidos`, `preco_ingredientes`
   - Suporta customização completa de ingredientes

3. **Novos Modelos**:
   - `Categoria`: Organização do cardápio
   - `Ingrediente`: Catálogo de ingredientes
   - `ProdutoVariacao`: Variações de tamanho/preço
   - `ProdutoIngrediente`: Ingredientes padrão dos produtos

### Mudanças na API
- Endpoint `/produtos/` agora retorna produtos com variações aninhadas
- Criar pedido requer `produto_variacao_id` ao invés de `produto_id`
- Novos endpoints públicos em `/cardapio/`
- Cálculo de preço automático com `/pedidos/calcular-preco`

## Regras de Negócio

### Customização de Pedidos
- **Adicionar ingredientes**: Soma `preco_adicional` ao preço base
- **Remover ingredientes**: Não altera preço, exceto ingredientes obrigatórios (não podem ser removidos)
- **Cálculo**: `preco_total = (preco_base + sum(preco_adicional)) × quantidade`

### Validações
- Ingrediente adicionado deve estar `disponivel=True`
- Ingrediente removido não pode ter `obrigatorio=True`
- Produto disponível = `produto.disponivel=True` E pelo menos uma `variacao.disponivel=True`

## Segurança

- Senhas criptografadas com bcrypt
- Autenticação via JWT (JSON Web Tokens)
- Tokens com expiração configurável
- CORS configurado para integração com frontend
- Controle de permissões por role (admin/usuário)
