# Backend - Sistema de Pizzaria

API RESTful desenvolvida com FastAPI para gerenciamento de pedidos de pizzaria.

## Funcionalidades

- **Autenticação JWT**: Sistema de login com access tokens e refresh tokens
- **Gerenciamento de Usuários**: Cadastro e autenticação de usuários
- **Gerenciamento de Pedidos**: Criação, listagem e atualização de pedidos
- **Itens de Pedido**: Controle detalhado de pizzas com sabor, tamanho e preço

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
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   └── models.py
│   ├── schemas/             # Schemas Pydantic
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── routers/             # Rotas da API
│       ├── __init__.py
│       ├── auth.py          # Autenticação
│       └── orders.py        # Pedidos
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Endpoints Principais

### Autenticação
- `POST /auth/criar_conta` - Criar nova conta
- `POST /auth/login` - Login (retorna access_token e refresh_token)

### Pedidos
- `GET /pedidos/` - Listar todos os pedidos
- `GET /pedidos/{id}` - Buscar pedido por ID
- `POST /pedidos/` - Criar novo pedido
- `PATCH /pedidos/{id}/status` - Atualizar status do pedido
- `DELETE /pedidos/{id}` - Cancelar pedido

## Modelo de Dados

### Usuário
- id, nome, email, senha (hash), ativo, admin

### Pedido
- id, status, usuario_id, preco_total
- Status: PENDENTE, EM_PREPARO, PRONTO, ENTREGUE, CANCELADO

### Item do Pedido
- id, pedido_id, quantidade, sabor, tamanho, preco_unitario, observacoes
- Tamanhos: PEQUENA, MEDIA, GRANDE, GIGANTE

## Segurança

- Senhas criptografadas com bcrypt
- Autenticação via JWT (JSON Web Tokens)
- Tokens com expiração configurável
- CORS configurado para integração com frontend
