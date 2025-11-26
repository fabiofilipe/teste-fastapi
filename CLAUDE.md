# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sistema completo de gerenciamento de pedidos para pizzaria, dividido em **backend** (FastAPI) e **frontend** (a ser implementado). O backend oferece API RESTful com autenticação JWT, gerenciamento de usuários e pedidos, usando SQLite como banco de dados.

## Project Structure

```
teste-fastapi/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py       # Aplicação FastAPI principal
│   │   ├── config.py     # Configurações e variáveis de ambiente
│   │   ├── database.py   # Setup do SQLAlchemy
│   │   ├── models/       # Modelos do banco de dados
│   │   ├── schemas/      # Schemas Pydantic
│   │   └── routers/      # Endpoints da API
│   ├── requirements.txt
│   ├── .env             # Variáveis de ambiente (gitignored)
│   └── README.md
├── frontend/            # Interface web (a ser implementado)
└── CLAUDE.md
```

## Development Commands

### Backend Setup and Running

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências do backend
cd backend
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com configurações apropriadas

# Executar servidor de desenvolvimento
uvicorn app.main:app --reload

# Especificar host e porta
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### API Documentation

Após iniciar o servidor:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Architecture

### Backend Structure (FastAPI)

O backend segue arquitetura modular com separação clara de responsabilidades:

**app/config.py**
- Gerenciamento de variáveis de ambiente via python-dotenv
- Configurações JWT (SECRET_KEY, ALGORITHM, expiração de tokens)
- DATABASE_URL configurável

**app/database.py**
- Engine SQLAlchemy (SQLite por padrão)
- Declarative Base para modelos ORM
- `get_db()`: Dependency para injeção de sessão do banco

**app/models/models.py** - Modelos SQLAlchemy com relationships:
- `Usuario`: Usuários do sistema com autenticação
- `Pedido`: Pedidos com status e preço total
- `ItemPedido`: Itens individuais (pizzas) de cada pedido

**app/schemas/schemas.py** - Schemas Pydantic para validação:
- `UsuarioSchema`, `UsuarioResponse`: Criação e resposta de usuários
- `LoginSchema`, `TokenResponse`: Autenticação
- `PedidoCreate`, `PedidoResponse`: Gestão de pedidos
- `ItemPedidoCreate`, `ItemPedidoResponse`: Itens de pedidos

**app/routers/auth.py** - Autenticação (`/auth`):
- `POST /auth/criar_conta`: Registro de usuário com hash bcrypt
- `POST /auth/login`: Retorna access_token (30min) e refresh_token (7 dias)
- Funções auxiliares: `criar_token()`, `autenticar_usuario()`

**app/routers/orders.py** - Pedidos (`/pedidos`):
- `GET /pedidos/`: Lista todos os pedidos
- `GET /pedidos/{id}`: Busca pedido específico
- `POST /pedidos/`: Cria novo pedido com itens
- `PATCH /pedidos/{id}/status`: Atualiza status do pedido
- `DELETE /pedidos/{id}`: Cancela pedido

**app/main.py** - Entry point:
- Inicialização do FastAPI com metadados
- Configuração CORS para integração frontend
- Registro de routers
- Criação automática de tabelas no banco

### Database Models

**Usuario**
- id, nome, email (unique), senha (hash bcrypt), ativo, admin
- Relationship: `pedidos` (one-to-many com Pedido)

**Pedido**
- id, status, usuario_id (FK), preco_total
- Status válidos: PENDENTE, EM_PREPARO, PRONTO, ENTREGUE, CANCELADO
- Relationships: `usuario` (many-to-one), `itens` (one-to-many com cascade delete)

**ItemPedido**
- id, pedido_id (FK), quantidade, sabor, tamanho, preco_unitario, observacoes
- Tamanhos válidos: PEQUENA, MEDIA, GRANDE, GIGANTE
- Relationship: `pedido` (many-to-one)

### Authentication Flow

1. **Registro** (`POST /auth/criar_conta`):
   - Valida email único
   - Hash de senha com bcrypt
   - Cria usuário no banco

2. **Login** (`POST /auth/login`):
   - `autenticar_usuario()`: Verifica email e senha
   - Valida se usuário está ativo
   - `criar_token()`: Gera JWT com claims `sub` (user_id) e `exp`
   - Retorna access_token e refresh_token

3. **Tokens JWT**:
   - Access token: Curta duração (padrão 30min)
   - Refresh token: Longa duração (padrão 7 dias)
   - Assinados com SECRET_KEY usando algoritmo configurável (padrão HS256)

### Environment Variables

Arquivo `.env` requerido no diretório `backend/`:

```bash
SECRET_KEY=sua_chave_secreta_forte
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=sqlite:///./banco.db
```

### Frontend (Planejado)

Status: 🚧 Em desenvolvimento

Diretório `frontend/` preparado para implementação com React/Vue/Angular. Ver `frontend/README.md` para detalhes.

### Important Notes

- O banco de dados é criado automaticamente na primeira execução via `Base.metadata.create_all()`
- CORS está configurado como `allow_origins=["*"]` - **ajustar em produção**
- Relacionamentos SQLAlchemy incluem cascade delete para manter integridade
- Pydantic v2 usa `pattern` (não `regex`) para validação de strings
- Email validation requer pacote `email-validator` (incluído no requirements.txt)
