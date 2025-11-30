# 🚀 PLANO DE MELHORIAS - SISTEMA DE GERENCIAMENTO DE PIZZARIA
## Roadmap para Transformação Enterprise Premium

> **Versão:** 1.0
> **Data:** 30/11/2025
> **Status Atual:** Protótipo Funcional (34% Enterprise-Ready)
> **Meta:** Sistema Enterprise Premium (95%+ Enterprise-Ready)

---

## 📊 ANÁLISE DO ESTADO ATUAL

### ✅ O QUE JÁ EXISTE E PODE SER REAPROVEITADO

#### **Backend - FastAPI (1.059 linhas de código)**

**Arquitetura Sólida:**
- ✅ Separação limpa: `models/`, `schemas/`, `routers/`
- ✅ Dependency Injection bem implementada
- ✅ Type hints completos em todo código
- ✅ Async/await onde apropriado
- ✅ RESTful API design

**Autenticação e Segurança:**
- ✅ Sistema JWT com access + refresh tokens
- ✅ Bcrypt para hash de senhas
- ✅ Sistema de roles (admin/user)
- ✅ Proteção de rotas por autenticação
- ✅ Validação de ownership (usuários só veem seus dados)
- ✅ Cálculo de preços server-side (anti-fraude)

**Tratamento de Erros (EXCELENTE):**
- ✅ 8 exceções customizadas específicas
- ✅ 5 handlers globais de erro
- ✅ Formato de resposta padronizado
- ✅ Status codes HTTP corretos

**Modelos de Dados:**
- ✅ Usuario (com roles e status ativo)
- ✅ Produto (com categorias, tamanhos, preços)
- ✅ Pedido (com status e validação)
- ✅ ItemPedido (com validação de preços)
- ✅ Relationships SQLAlchemy bem configuradas

**Endpoints Implementados:**
- ✅ `/auth/*` - Registro, login, refresh token
- ✅ `/pedidos/*` - CRUD completo com validações
- ✅ `/produtos/*` - CRUD completo com filtros
- ✅ `/health`, `/metrics`, `/status` - Monitoramento

**Validação:**
- ✅ Pydantic v2 com validações robustas
- ✅ Email validation
- ✅ Constraints (min, max, pattern)
- ✅ Business logic validation

**Documentação:**
- ✅ README.md detalhado
- ✅ CLAUDE.md para AI assistants
- ✅ Changelog (atualizações_26-11.md)
- ✅ Swagger UI e ReDoc automáticos
- ✅ Docstrings em funções importantes

### ❌ GAPS CRÍTICOS IDENTIFICADOS

#### **Testes: 0/10** ⚠️ CRÍTICO
- ❌ Zero testes unitários
- ❌ Zero testes de integração
- ❌ Zero coverage

#### **DevOps: 0/10** ⚠️ CRÍTICO
- ❌ Sem Docker/Docker Compose
- ❌ Sem CI/CD pipeline
- ❌ Sem migrations (Alembic)

#### **Logging: 0/10** ⚠️ ALTO
- ❌ Sem logging estruturado
- ❌ Sem correlation IDs
- ❌ Sem integração com ferramentas de monitoring

#### **Segurança: 4/10** ⚠️ ALTO
- ❌ CORS permite qualquer origem (`*`)
- ❌ Sem rate limiting
- ❌ Sem token blacklist (logout não invalida)
- ❌ Sem validação de força de senha
- ❌ SECRET_KEY fraca

#### **Database: 3/10** ⚠️ ALTO
- ❌ SQLite (não escalável)
- ❌ Sem migrations system
- ❌ Sem timestamps (created_at, updated_at)
- ❌ Sem soft deletes

#### **Performance: 4/10** ⚠️ MÉDIO
- ❌ Sem cache (Redis)
- ❌ Sem paginação
- ❌ Sem query optimization
- ❌ Sem background tasks

#### **Frontend: 0/10**
- ❌ 100% não implementado

---

## 🎯 VISÃO GERAL DO PLANO

### **Objetivo Final**
Transformar o protótipo atual em um sistema enterprise-grade comparável a plataformas como iFood, Rappi ou Uber Eats (em escala de pizzaria), com:

- 🏗️ **Arquitetura**: Microserviços escaláveis com Docker/Kubernetes
- 🔒 **Segurança**: Enterprise-grade com compliance LGPD/GDPR
- 📊 **Observabilidade**: Logging, metrics, tracing, alerting
- ⚡ **Performance**: Cache, CDN, otimização de queries, <200ms response time
- 🧪 **Qualidade**: >85% test coverage, CI/CD, code quality gates
- 🎨 **UX Premium**: Interface moderna, responsiva, acessível, PWA
- 💳 **Pagamentos**: Integração com gateways (Stripe, Mercado Pago, PayPal)
- 📱 **Notificações**: Email, SMS, Push notifications, WhatsApp
- 📈 **Analytics**: Dashboard executivo com KPIs em tempo real

### **Metodologia**
- ✅ Desenvolvimento incremental por fases
- ✅ Cada fase entrega valor e pode ir para produção
- ✅ Testes automatizados desde a Fase 1
- ✅ Documentação contínua
- ✅ Code review obrigatório

### **Timeline Estimado**
- **Fase 1-2:** 2-3 meses (Fundação + Segurança)
- **Fase 3-4:** 2-3 meses (Infraestrutura + Performance)
- **Fase 5-6:** 3-4 meses (Features + Frontend)
- **Fase 7-8:** 2-3 meses (Avançado + DevOps)
- **TOTAL:** 9-13 meses (1-2 devs full-time)

---

## 📋 FASES DE IMPLEMENTAÇÃO

---

## **FASE 1: FUNDAÇÃO E QUALIDADE** ⚠️ PRIORIDADE CRÍTICA
**Objetivo:** Estabelecer base sólida para desenvolvimento confiável
**Duração:** 3-4 semanas
**Pré-requisito para:** Todas as fases seguintes

### **1.1 - Setup de Testes Automatizados** ⚠️ URGENTE

**Dependências:**
```bash
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
httpx==0.25.2  # Cliente HTTP async para testes
faker==21.0.0  # Dados fake para testes
factory-boy==3.3.0  # Factories para modelos
```

**Tasks:**
1. [ ] Criar estrutura de diretórios
   ```
   backend/
   ├── tests/
   │   ├── __init__.py
   │   ├── conftest.py           # Fixtures globais
   │   ├── factories.py          # Factories para modelos
   │   ├── unit/
   │   │   ├── test_models.py    # Testes de modelos
   │   │   ├── test_schemas.py   # Testes de schemas
   │   │   └── test_utils.py     # Testes de utilitários
   │   └── integration/
   │       ├── test_auth.py      # Testes de autenticação
   │       ├── test_orders.py    # Testes de pedidos
   │       ├── test_products.py  # Testes de produtos
   │       └── test_health.py    # Testes de health checks
   ```

2. [ ] Configurar `pytest.ini`
   ```ini
   [pytest]
   testpaths = tests
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   addopts =
       --strict-markers
       --cov=app
       --cov-report=html
       --cov-report=term-missing
       --cov-fail-under=80
       -v
   asyncio_mode = auto
   ```

3. [ ] Criar `conftest.py` com fixtures essenciais
   - Fixture de database de teste (SQLite in-memory)
   - Fixture de cliente HTTP (TestClient)
   - Fixture de usuário autenticado
   - Fixture de admin autenticado
   - Fixture de produtos de teste

4. [ ] Escrever testes unitários (objetivo: 50+ testes)
   - Testes de criação de modelos
   - Testes de validação de schemas
   - Testes de hash de senha
   - Testes de criação de tokens
   - Testes de validação de permissões

5. [ ] Escrever testes de integração (objetivo: 30+ testes)
   - Fluxo completo de registro de usuário
   - Fluxo completo de login
   - Fluxo completo de criação de pedido
   - Fluxo completo de atualização de produto
   - Testes de permissões (admin vs user)
   - Testes de erros (404, 401, 403, 422)

6. [ ] Configurar coverage mínimo: 80%

7. [ ] Criar script de execução
   ```bash
   # backend/run_tests.sh
   #!/bin/bash
   pytest tests/ -v --cov=app --cov-report=html --cov-report=term
   ```

**Critérios de Aceitação:**
- ✅ Mínimo 80 testes implementados
- ✅ Coverage ≥ 80%
- ✅ Todos os testes passando
- ✅ Tempo de execução < 30 segundos

---

### **1.2 - Docker e Containerização** ⚠️ URGENTE

**Tasks:**

1. [ ] Criar `Dockerfile` multi-stage para backend
   ```dockerfile
   # backend/Dockerfile
   # Stage 1: Build
   FROM python:3.11-slim as builder
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir --user -r requirements.txt

   # Stage 2: Runtime
   FROM python:3.11-slim
   WORKDIR /app
   COPY --from=builder /root/.local /root/.local
   COPY ./app ./app
   ENV PATH=/root/.local/bin:$PATH
   EXPOSE 8000
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. [ ] Criar `.dockerignore`
   ```
   __pycache__
   *.pyc
   *.pyo
   *.pyd
   .Python
   venv/
   .env
   .venv
   banco.db
   .pytest_cache
   .coverage
   htmlcov/
   *.log
   .git
   .gitignore
   README.md
   ```

3. [ ] Criar `docker-compose.yml` para desenvolvimento
   ```yaml
   version: '3.8'

   services:
     postgres:
       image: postgres:15-alpine
       container_name: pizzaria-db
       environment:
         POSTGRES_DB: pizzaria
         POSTGRES_USER: admin
         POSTGRES_PASSWORD: dev_password_123
       ports:
         - "5432:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data
       healthcheck:
         test: ["CMD-SHELL", "pg_isready -U admin"]
         interval: 10s
         timeout: 5s
         retries: 5

     redis:
       image: redis:7-alpine
       container_name: pizzaria-redis
       ports:
         - "6379:6379"
       volumes:
         - redis_data:/data
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 10s
         timeout: 5s
         retries: 5

     backend:
       build:
         context: ./backend
         dockerfile: Dockerfile
       container_name: pizzaria-api
       environment:
         DATABASE_URL: postgresql://admin:dev_password_123@postgres:5432/pizzaria
         REDIS_URL: redis://redis:6379/0
         SECRET_KEY: ${SECRET_KEY}
         ENVIRONMENT: development
       ports:
         - "8000:8000"
       volumes:
         - ./backend/app:/app/app
       depends_on:
         postgres:
           condition: service_healthy
         redis:
           condition: service_healthy
       command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

     pgadmin:
       image: dpage/pgadmin4:latest
       container_name: pizzaria-pgadmin
       environment:
         PGADMIN_DEFAULT_EMAIL: admin@pizzaria.com
         PGADMIN_DEFAULT_PASSWORD: admin
       ports:
         - "5050:80"
       depends_on:
         - postgres

   volumes:
     postgres_data:
     redis_data:
   ```

4. [ ] Criar `docker-compose.prod.yml` para produção
   ```yaml
   version: '3.8'

   services:
     backend:
       build:
         context: ./backend
         dockerfile: Dockerfile
         target: runtime
       restart: unless-stopped
       environment:
         DATABASE_URL: ${DATABASE_URL}
         REDIS_URL: ${REDIS_URL}
         SECRET_KEY: ${SECRET_KEY}
         ENVIRONMENT: production
       ports:
         - "8000:8000"
       command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

5. [ ] Criar `Makefile` para comandos comuns
   ```makefile
   .PHONY: help build up down logs test clean

   help:
       @echo "Comandos disponíveis:"
       @echo "  make build      - Build das imagens Docker"
       @echo "  make up         - Sobe os containers"
       @echo "  make down       - Para os containers"
       @echo "  make logs       - Mostra logs"
       @echo "  make test       - Roda os testes"
       @echo "  make clean      - Limpa volumes e imagens"

   build:
       docker-compose build

   up:
       docker-compose up -d

   down:
       docker-compose down

   logs:
       docker-compose logs -f

   test:
       docker-compose exec backend pytest tests/ -v

   clean:
       docker-compose down -v
       docker system prune -f
   ```

6. [ ] Atualizar `README.md` com instruções Docker

**Critérios de Aceitação:**
- ✅ `docker-compose up` funciona sem erros
- ✅ API acessível em `http://localhost:8000`
- ✅ PostgreSQL funcionando
- ✅ Redis funcionando
- ✅ Health checks passando

---

### **1.3 - Database Migrations com Alembic**

**Dependências:**
```bash
alembic==1.13.1
psycopg2-binary==2.9.9  # Driver PostgreSQL
```

**Tasks:**

1. [ ] Instalar e inicializar Alembic
   ```bash
   cd backend
   alembic init alembic
   ```

2. [ ] Configurar `alembic.ini`
   ```ini
   [alembic]
   script_location = alembic
   prepend_sys_path = .
   sqlalchemy.url = postgresql://admin:dev_password_123@localhost:5432/pizzaria
   ```

3. [ ] Atualizar `alembic/env.py` para usar models
   ```python
   from app.database import Base
   from app.models.models import *
   target_metadata = Base.metadata
   ```

4. [ ] Criar migration inicial
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

5. [ ] Adicionar timestamps aos modelos
   ```python
   # Em models.py
   from sqlalchemy import func

   class Usuario(Base):
       # ... campos existentes ...
       created_at = Column(DateTime, server_default=func.now())
       updated_at = Column(DateTime, onupdate=func.now())
   ```

6. [ ] Criar migrations para timestamps
   ```bash
   alembic revision --autogenerate -m "Add timestamps to all models"
   ```

7. [ ] Criar script de seed data
   ```python
   # backend/scripts/seed.py
   from app.database import SessionLocal
   from app.models.models import Usuario, Produto
   import bcrypt

   def seed_database():
       db = SessionLocal()

       # Criar usuário admin padrão
       admin = Usuario(
           nome="Admin",
           email="admin@pizzaria.com",
           senha=bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode(),
           admin=True,
           ativo=True
       )
       db.add(admin)

       # Criar produtos de exemplo
       produtos = [
           Produto(nome="Margherita", categoria="PIZZA", tamanho="MEDIA", preco=35.00),
           Produto(nome="Calabresa", categoria="PIZZA", tamanho="GRANDE", preco=45.00),
           # ... mais produtos
       ]
       db.add_all(produtos)
       db.commit()
   ```

**Critérios de Aceitação:**
- ✅ Migrations funcionando
- ✅ PostgreSQL como database principal
- ✅ Todos os modelos com timestamps
- ✅ Seed data script funcional

---

### **1.4 - Linting e Code Quality**

**Dependências:**
```bash
black==23.12.1
flake8==7.0.0
ruff==0.1.9
mypy==1.8.0
isort==5.13.2
pre-commit==3.6.0
```

**Tasks:**

1. [ ] Criar `pyproject.toml`
   ```toml
   [tool.black]
   line-length = 100
   target-version = ['py311']
   include = '\.pyi?$'

   [tool.isort]
   profile = "black"
   line_length = 100

   [tool.mypy]
   python_version = "3.11"
   warn_return_any = true
   warn_unused_configs = true
   disallow_untyped_defs = true

   [tool.ruff]
   line-length = 100
   target-version = "py311"
   select = ["E", "F", "I", "N", "W"]
   ```

2. [ ] Criar `.flake8`
   ```ini
   [flake8]
   max-line-length = 100
   exclude = .git,__pycache__,venv,.venv,alembic
   ignore = E203, W503
   ```

3. [ ] Criar `.pre-commit-config.yaml`
   ```yaml
   repos:
     - repo: https://github.com/pre-commit/pre-commit-hooks
       rev: v4.5.0
       hooks:
         - id: trailing-whitespace
         - id: end-of-file-fixer
         - id: check-yaml
         - id: check-added-large-files

     - repo: https://github.com/psf/black
       rev: 23.12.1
       hooks:
         - id: black

     - repo: https://github.com/pycqa/isort
       rev: 5.13.2
       hooks:
         - id: isort

     - repo: https://github.com/pycqa/flake8
       rev: 7.0.0
       hooks:
         - id: flake8
   ```

4. [ ] Instalar pre-commit hooks
   ```bash
   pre-commit install
   ```

5. [ ] Formatar código existente
   ```bash
   black backend/app
   isort backend/app
   ```

6. [ ] Corrigir issues do flake8/ruff
   ```bash
   ruff check backend/app --fix
   ```

**Critérios de Aceitação:**
- ✅ Todo código formatado com black
- ✅ Imports organizados com isort
- ✅ Zero warnings do flake8
- ✅ Pre-commit hooks instalados

---

### **1.5 - Documentação Técnica**

**Tasks:**

1. [ ] Criar `ARCHITECTURE.md`
   - Diagrama de arquitetura
   - Fluxo de dados
   - Decisões arquiteturais

2. [ ] Criar `DEPLOYMENT.md`
   - Requisitos de infraestrutura
   - Variáveis de ambiente
   - Processo de deploy
   - Rollback procedures

3. [ ] Criar `CONTRIBUTING.md`
   - Guia de contribuição
   - Padrões de código
   - Process de PR/MR
   - Commit message conventions

4. [ ] Criar `SECURITY.md`
   - Política de segurança
   - Como reportar vulnerabilidades
   - Disclosure policy

5. [ ] Criar diagramas
   - Diagrama ER (database)
   - Diagrama de sequência (fluxos principais)
   - Diagrama de componentes

6. [ ] Criar Postman/Insomnia collection
   - Todos os endpoints
   - Variáveis de ambiente
   - Testes automatizados

**Entregáveis:**
```
docs/
├── architecture/
│   ├── overview.md
│   ├── database-schema.png
│   └── component-diagram.png
├── api/
│   ├── postman-collection.json
│   └── insomnia-workspace.json
└── deployment/
    ├── docker.md
    └── kubernetes.md
```

---

### **✅ CHECKLIST FASE 1**

- [ ] 80+ testes implementados com ≥80% coverage
- [ ] Docker Compose funcionando (backend + postgres + redis)
- [ ] Migrations Alembic configuradas
- [ ] Linting e formatação automáticos (pre-commit)
- [ ] Documentação técnica completa
- [ ] CI/CD básico (próxima fase)

**Resultado Esperado:**
Base sólida para desenvolvimento com qualidade, permitindo deploy confiável.

---

## **FASE 2: SEGURANÇA ENTERPRISE** ⚠️ PRIORIDADE ALTA
**Objetivo:** Elevar segurança ao nível enterprise
**Duração:** 2-3 semanas
**Depende de:** Fase 1

### **2.1 - Correções Críticas de Segurança**

**Dependências:**
```bash
slowapi==0.1.9  # Rate limiting
redis==5.0.1  # Cache e blacklist
python-jose[cryptography]==3.5.0  # JWT melhorado
secrets  # Geração de chaves seguras (built-in)
```

**Tasks:**

1. [ ] **Configurar CORS adequadamente**
   ```python
   # app/main.py
   from fastapi.middleware.cors import CORSMiddleware

   allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

   app.add_middleware(
       CORSMiddleware,
       allow_origins=allowed_origins,  # ❌ NÃO usar ["*"]
       allow_credentials=True,
       allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
       allow_headers=["*"],
   )
   ```

2. [ ] **Implementar Rate Limiting**
   ```python
   # app/middleware/rate_limit.py
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   from slowapi.errors import RateLimitExceeded

   limiter = Limiter(key_func=get_remote_address)

   # Em routers/auth.py
   @router.post("/login")
   @limiter.limit("5/minute")  # Máximo 5 tentativas por minuto
   async def login(...):
       ...
   ```

3. [ ] **Implementar Token Blacklist com Redis**
   ```python
   # app/services/token_blacklist.py
   import redis
   from datetime import timedelta

   redis_client = redis.from_url(os.getenv("REDIS_URL"))

   def blacklist_token(token: str, expires_in: int):
       """Adiciona token à blacklist"""
       redis_client.setex(
           f"blacklist:{token}",
           timedelta(seconds=expires_in),
           "1"
       )

   def is_token_blacklisted(token: str) -> bool:
       """Verifica se token está na blacklist"""
       return redis_client.exists(f"blacklist:{token}") > 0
   ```

4. [ ] **Implementar Logout Funcional**
   ```python
   @router.post("/logout")
   async def logout(
       token: str = Depends(oauth2_scheme),
       db: Session = Depends(get_db)
   ):
       # Decodificar token para pegar exp
       payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
       exp = payload.get("exp")

       # Adicionar à blacklist até expirar
       blacklist_token(token, exp - int(time.time()))

       return {"message": "Logout realizado com sucesso"}
   ```

5. [ ] **Validação de Força de Senha**
   ```python
   # app/utils/password.py
   import re

   def validate_password_strength(password: str) -> tuple[bool, str]:
       """Valida força da senha"""
       if len(password) < 8:
           return False, "Senha deve ter no mínimo 8 caracteres"

       if not re.search(r"[A-Z]", password):
           return False, "Senha deve conter letra maiúscula"

       if not re.search(r"[a-z]", password):
           return False, "Senha deve conter letra minúscula"

       if not re.search(r"\d", password):
           return False, "Senha deve conter número"

       if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
           return False, "Senha deve conter caractere especial"

       return True, "Senha válida"
   ```

6. [ ] **Account Lockout após tentativas falhadas**
   ```python
   # app/services/auth_security.py
   from datetime import datetime, timedelta

   MAX_LOGIN_ATTEMPTS = 5
   LOCKOUT_DURATION = 15  # minutos

   def record_failed_login(email: str, redis_client):
       """Registra tentativa falhada"""
       key = f"failed_login:{email}"
       attempts = redis_client.incr(key)

       if attempts == 1:
           redis_client.expire(key, LOCKOUT_DURATION * 60)

       return attempts

   def is_account_locked(email: str, redis_client) -> bool:
       """Verifica se conta está bloqueada"""
       attempts = redis_client.get(f"failed_login:{email}")
       return int(attempts or 0) >= MAX_LOGIN_ATTEMPTS
   ```

7. [ ] **Gerar SECRET_KEY forte**
   ```python
   # Script para gerar chave
   import secrets
   print(secrets.token_urlsafe(64))  # 512 bits
   ```

8. [ ] **Headers de Segurança**
   ```python
   # app/middleware/security_headers.py
   from fastapi import Request
   from starlette.middleware.base import BaseHTTPMiddleware

   class SecurityHeadersMiddleware(BaseHTTPMiddleware):
       async def dispatch(self, request: Request, call_next):
           response = await call_next(request)

           response.headers["X-Content-Type-Options"] = "nosniff"
           response.headers["X-Frame-Options"] = "DENY"
           response.headers["X-XSS-Protection"] = "1; mode=block"
           response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
           response.headers["Content-Security-Policy"] = "default-src 'self'"

           return response
   ```

**Critérios de Aceitação:**
- ✅ CORS configurado corretamente
- ✅ Rate limiting em endpoints sensíveis
- ✅ Logout invalida tokens
- ✅ Senha forte obrigatória
- ✅ Lockout após 5 tentativas falhadas
- ✅ Headers de segurança configurados

---

### **2.2 - Autenticação Avançada**

**Dependências:**
```bash
fastapi-mail==1.4.1  # Envio de emails
itsdangerous==2.1.2  # Tokens temporários
jinja2==3.1.2  # Templates de email
```

**Tasks:**

1. [ ] **Forgot Password / Reset Password**
   ```python
   @router.post("/forgot-password")
   async def forgot_password(email: EmailStr, db: Session = Depends(get_db)):
       user = db.query(Usuario).filter(Usuario.email == email).first()

       if not user:
           # Não revelar se email existe
           return {"message": "Se o email existir, um link será enviado"}

       # Gerar token temporário (expira em 1 hora)
       reset_token = create_reset_token(user.id)

       # Enviar email
       send_password_reset_email(user.email, reset_token)

       return {"message": "Email enviado com sucesso"}

   @router.post("/reset-password")
   async def reset_password(
       token: str,
       new_password: str,
       db: Session = Depends(get_db)
   ):
       # Validar token
       user_id = verify_reset_token(token)
       if not user_id:
           raise HTTPException(status_code=400, detail="Token inválido ou expirado")

       # Validar força da senha
       valid, message = validate_password_strength(new_password)
       if not valid:
           raise HTTPException(status_code=400, detail=message)

       # Atualizar senha
       user = db.query(Usuario).filter(Usuario.id == user_id).first()
       user.senha = hash_password(new_password)
       db.commit()

       return {"message": "Senha alterada com sucesso"}
   ```

2. [ ] **Email Verification**
   ```python
   # Adicionar campo ao modelo Usuario
   email_verified = Column(Boolean, default=False)
   verification_token = Column(String, nullable=True)

   @router.post("/verify-email/{token}")
   async def verify_email(token: str, db: Session = Depends(get_db)):
       user = db.query(Usuario).filter(
           Usuario.verification_token == token
       ).first()

       if not user:
           raise HTTPException(status_code=400, detail="Token inválido")

       user.email_verified = True
       user.verification_token = None
       db.commit()

       return {"message": "Email verificado com sucesso"}
   ```

3. [ ] **Change Password (usuário logado)**
   ```python
   @router.post("/change-password")
   async def change_password(
       current_password: str,
       new_password: str,
       user: Usuario = Depends(get_current_user),
       db: Session = Depends(get_db)
   ):
       # Verificar senha atual
       if not verify_password(current_password, user.senha):
           raise HTTPException(status_code=400, detail="Senha atual incorreta")

       # Validar nova senha
       valid, message = validate_password_strength(new_password)
       if not valid:
           raise HTTPException(status_code=400, detail=message)

       # Atualizar
       user.senha = hash_password(new_password)
       db.commit()

       return {"message": "Senha alterada com sucesso"}
   ```

4. [ ] **Configurar envio de emails**
   ```python
   # app/services/email.py
   from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

   conf = ConnectionConfig(
       MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
       MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
       MAIL_FROM=os.getenv("MAIL_FROM"),
       MAIL_PORT=587,
       MAIL_SERVER=os.getenv("MAIL_SERVER"),
       MAIL_STARTTLS=True,
       MAIL_SSL_TLS=False,
   )

   async def send_email(to: str, subject: str, body: str):
       message = MessageSchema(
           subject=subject,
           recipients=[to],
           body=body,
           subtype="html"
       )

       fm = FastMail(conf)
       await fm.send_message(message)
   ```

5. [ ] **Templates de email**
   ```html
   <!-- templates/emails/reset_password.html -->
   <!DOCTYPE html>
   <html>
   <head>
       <style>
           /* Estilos inline para compatibilidade com clients de email */
       </style>
   </head>
   <body>
       <h2>Redefinição de Senha</h2>
       <p>Olá {{ user_name }},</p>
       <p>Recebemos uma solicitação para redefinir sua senha.</p>
       <a href="{{ reset_link }}" style="...">Redefinir Senha</a>
       <p>Este link expira em 1 hora.</p>
   </body>
   </html>
   ```

**Critérios de Aceitação:**
- ✅ Forgot password funcional
- ✅ Reset password funcional
- ✅ Email verification implementado
- ✅ Change password funcional
- ✅ Emails enviados corretamente

---

### **2.3 - Audit Logging**

**Tasks:**

1. [ ] **Criar modelo de AuditLog**
   ```python
   # app/models/models.py
   class AuditLog(Base):
       __tablename__ = "audit_logs"

       id = Column(Integer, primary_key=True, index=True)
       user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
       action = Column(String, nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, etc
       entity_type = Column(String, nullable=False)  # Usuario, Pedido, Produto
       entity_id = Column(Integer, nullable=True)
       old_value = Column(JSON, nullable=True)
       new_value = Column(JSON, nullable=True)
       ip_address = Column(String, nullable=True)
       user_agent = Column(String, nullable=True)
       timestamp = Column(DateTime, server_default=func.now())
   ```

2. [ ] **Middleware de Audit Logging**
   ```python
   # app/middleware/audit.py
   async def log_audit_event(
       db: Session,
       user_id: int,
       action: str,
       entity_type: str,
       entity_id: int = None,
       old_value: dict = None,
       new_value: dict = None,
       request: Request = None
   ):
       audit = AuditLog(
           user_id=user_id,
           action=action,
           entity_type=entity_type,
           entity_id=entity_id,
           old_value=old_value,
           new_value=new_value,
           ip_address=request.client.host if request else None,
           user_agent=request.headers.get("user-agent") if request else None
       )
       db.add(audit)
       db.commit()
   ```

3. [ ] **Integrar em ações críticas**
   - Login/Logout
   - Criação/Atualização de usuários
   - Criação/Atualização de pedidos
   - Mudanças de status de pedido
   - Ações administrativas

**Critérios de Aceitação:**
- ✅ Todas ações críticas logadas
- ✅ Logs contêm informações suficientes
- ✅ Endpoint admin para consultar logs

---

### **✅ CHECKLIST FASE 2**

- [ ] CORS configurado corretamente
- [ ] Rate limiting implementado
- [ ] Token blacklist funcional
- [ ] Validação de senha forte
- [ ] Account lockout implementado
- [ ] Forgot/Reset password funcional
- [ ] Email verification implementado
- [ ] Audit logging completo
- [ ] Headers de segurança configurados
- [ ] Testes de segurança implementados

**Resultado Esperado:**
Sistema com segurança enterprise-grade, pronto para compliance LGPD/GDPR.

---

## **FASE 3: LOGGING, MONITORING E OBSERVABILIDADE**
**Objetivo:** Visibilidade completa do sistema
**Duração:** 2 semanas
**Depende de:** Fase 1

### **3.1 - Structured Logging**

**Dependências:**
```bash
python-json-logger==2.0.7
loguru==0.7.2  # Alternativa moderna
```

**Tasks:**

1. [ ] **Configurar logging estruturado**
   ```python
   # app/logging_config.py
   import logging
   from pythonjsonlogger import jsonlogger
   import os

   def setup_logging():
       log_level = os.getenv("LOG_LEVEL", "INFO")

       logger = logging.getLogger()
       logger.setLevel(log_level)

       # Handler para stdout (JSON)
       handler = logging.StreamHandler()
       formatter = jsonlogger.JsonFormatter(
           "%(timestamp)s %(level)s %(name)s %(message)s %(correlation_id)s"
       )
       handler.setFormatter(formatter)
       logger.addHandler(handler)

       return logger
   ```

2. [ ] **Middleware de Correlation ID**
   ```python
   # app/middleware/correlation_id.py
   import uuid
   from contextvars import ContextVar

   correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")

   class CorrelationIdMiddleware(BaseHTTPMiddleware):
       async def dispatch(self, request: Request, call_next):
           correlation_id = request.headers.get(
               "X-Correlation-ID",
               str(uuid.uuid4())
           )
           correlation_id_var.set(correlation_id)

           response = await call_next(request)
           response.headers["X-Correlation-ID"] = correlation_id

           return response
   ```

3. [ ] **Request/Response Logging**
   ```python
   # app/middleware/logging.py
   import time

   class RequestLoggingMiddleware(BaseHTTPMiddleware):
       async def dispatch(self, request: Request, call_next):
           start_time = time.time()

           # Log request
           logger.info(
               "Request started",
               extra={
                   "method": request.method,
                   "path": request.url.path,
                   "correlation_id": correlation_id_var.get()
               }
           )

           response = await call_next(request)

           # Log response
           duration = time.time() - start_time
           logger.info(
               "Request completed",
               extra={
                   "method": request.method,
                   "path": request.url.path,
                   "status_code": response.status_code,
                   "duration_ms": duration * 1000,
                   "correlation_id": correlation_id_var.get()
               }
           )

           return response
   ```

4. [ ] **Sensitive Data Masking**
   ```python
   # app/utils/logging.py
   def mask_sensitive_data(data: dict) -> dict:
       """Mascara dados sensíveis em logs"""
       sensitive_fields = ["senha", "password", "token", "cpf", "credit_card"]

       masked = data.copy()
       for key in masked:
           if any(field in key.lower() for field in sensitive_fields):
               masked[key] = "***MASKED***"

       return masked
   ```

**Critérios de Aceitação:**
- ✅ Logs em formato JSON estruturado
- ✅ Correlation IDs em todas requisições
- ✅ Request/response logging automático
- ✅ Dados sensíveis mascarados

---

### **3.2 - Error Tracking com Sentry**

**Dependências:**
```bash
sentry-sdk[fastapi]==1.39.2
```

**Tasks:**

1. [ ] **Configurar Sentry**
   ```python
   # app/main.py
   import sentry_sdk
   from sentry_sdk.integrations.fastapi import FastApiIntegration

   sentry_sdk.init(
       dsn=os.getenv("SENTRY_DSN"),
       integrations=[FastApiIntegration()],
       environment=os.getenv("ENVIRONMENT", "development"),
       traces_sample_rate=1.0 if os.getenv("ENVIRONMENT") == "development" else 0.1,
       send_default_pii=False,  # Não enviar PII
   )
   ```

2. [ ] **Contexto adicional em erros**
   ```python
   from sentry_sdk import set_user, set_context

   # Em dependency de autenticação
   def add_sentry_context(user: Usuario):
       set_user({"id": user.id, "email": user.email})
       set_context("user_info", {
           "admin": user.admin,
           "ativo": user.ativo
       })
   ```

3. [ ] **Alertas customizados**
   - Configurar alertas no Sentry
   - Integrar com Slack/Discord
   - Definir thresholds

**Critérios de Aceitação:**
- ✅ Erros capturados automaticamente
- ✅ Stack traces completos
- ✅ Contexto de usuário em erros
- ✅ Alertas configurados

---

### **3.3 - Métricas com Prometheus**

**Dependências:**
```bash
prometheus-client==0.19.0
prometheus-fastapi-instrumentator==6.1.0
```

**Tasks:**

1. [ ] **Configurar Prometheus**
   ```python
   # app/main.py
   from prometheus_fastapi_instrumentator import Instrumentator

   instrumentator = Instrumentator()
   instrumentator.instrument(app).expose(app, endpoint="/metrics")
   ```

2. [ ] **Métricas customizadas**
   ```python
   # app/metrics.py
   from prometheus_client import Counter, Histogram, Gauge

   # Contadores
   pedidos_criados = Counter(
       "pedidos_criados_total",
       "Total de pedidos criados",
       ["status"]
   )

   # Histogramas (latência)
   request_duration = Histogram(
       "request_duration_seconds",
       "Duração das requisições",
       ["method", "endpoint"]
   )

   # Gauges
   usuarios_ativos = Gauge(
       "usuarios_ativos",
       "Número de usuários ativos"
   )
   ```

3. [ ] **Dashboard Grafana**
   - Criar docker-compose para Grafana
   - Importar dashboards prontos
   - Criar dashboards customizados
   - Configurar alertas

**Critérios de Aceitação:**
- ✅ Métricas básicas expostas
- ✅ Métricas de negócio implementadas
- ✅ Grafana funcionando
- ✅ Dashboards criados

---

### **✅ CHECKLIST FASE 3**

- [ ] Logging estruturado (JSON)
- [ ] Correlation IDs implementados
- [ ] Sentry configurado e funcionando
- [ ] Prometheus metrics expostas
- [ ] Grafana dashboards criados
- [ ] Alertas configurados
- [ ] Documentação de observabilidade

**Resultado Esperado:**
Visibilidade completa do sistema, troubleshooting rápido, detecção proativa de problemas.

---

## **FASE 4: PERFORMANCE E ESCALABILIDADE**
**Objetivo:** Sistema rápido e escalável
**Duração:** 2-3 semanas
**Depende de:** Fase 1

### **4.1 - Cache com Redis**

**Tasks:**

1. [ ] **Setup Redis cache**
   ```python
   # app/cache.py
   import redis.asyncio as redis
   import json
   from functools import wraps

   redis_client = redis.from_url(os.getenv("REDIS_URL"))

   def cached(ttl: int = 300):
       """Decorator para cache de funções"""
       def decorator(func):
           @wraps(func)
           async def wrapper(*args, **kwargs):
               # Gerar chave de cache
               cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

               # Tentar buscar do cache
               cached_value = await redis_client.get(cache_key)
               if cached_value:
                   return json.loads(cached_value)

               # Executar função
               result = await func(*args, **kwargs)

               # Salvar no cache
               await redis_client.setex(
                   cache_key,
                   ttl,
                   json.dumps(result)
               )

               return result
           return wrapper
       return decorator
   ```

2. [ ] **Cachear listagens**
   ```python
   @router.get("/produtos/")
   @cached(ttl=600)  # 10 minutos
   async def listar_produtos(...):
       ...
   ```

3. [ ] **Invalidar cache quando necessário**
   ```python
   @router.post("/produtos/")
   async def criar_produto(...):
       # ... criar produto ...

       # Invalidar cache
       await redis_client.delete("listar_produtos:*")
   ```

4. [ ] **Cache de sessões de usuário**

**Critérios de Aceitação:**
- ✅ Cache funcionando para listagens
- ✅ Invalidação automática
- ✅ TTL configurável
- ✅ Performance melhorada em 50%+

---

### **4.2 - Paginação**

**Tasks:**

1. [ ] **Criar schema de paginação**
   ```python
   # app/schemas/pagination.py
   from typing import Generic, TypeVar, List
   from pydantic import BaseModel

   T = TypeVar("T")

   class PaginatedResponse(BaseModel, Generic[T]):
       items: List[T]
       total: int
       page: int
       page_size: int
       total_pages: int
   ```

2. [ ] **Implementar paginação em listagens**
   ```python
   @router.get("/pedidos/", response_model=PaginatedResponse[PedidoResponse])
   async def listar_pedidos(
       page: int = Query(1, ge=1),
       page_size: int = Query(20, ge=1, le=100),
       db: Session = Depends(get_db)
   ):
       offset = (page - 1) * page_size

       total = db.query(Pedido).count()
       pedidos = db.query(Pedido).offset(offset).limit(page_size).all()

       return PaginatedResponse(
           items=pedidos,
           total=total,
           page=page,
           page_size=page_size,
           total_pages=(total + page_size - 1) // page_size
       )
   ```

**Critérios de Aceitação:**
- ✅ Paginação em todas listagens
- ✅ Parâmetros configuráveis
- ✅ Metadados de paginação corretos

---

### **4.3 - Otimização de Queries**

**Tasks:**

1. [ ] **Adicionar índices estratégicos**
   ```python
   # Em models.py
   class Pedido(Base):
       __tablename__ = "pedidos"
       # ... campos ...

       __table_args__ = (
           Index("ix_pedidos_usuario_status", "usuario_id", "status"),
           Index("ix_pedidos_created_at", "created_at"),
       )
   ```

2. [ ] **Eager loading para evitar N+1**
   ```python
   from sqlalchemy.orm import joinedload

   pedidos = db.query(Pedido)\
       .options(joinedload(Pedido.itens))\
       .options(joinedload(Pedido.usuario))\
       .all()
   ```

3. [ ] **Query optimization**
   - Selects específicos (não `SELECT *`)
   - Limit/offset adequados
   - Joins otimizados

4. [ ] **Connection pooling**
   ```python
   # app/database.py
   engine = create_engine(
       DATABASE_URL,
       pool_size=20,
       max_overflow=0,
       pool_pre_ping=True
   )
   ```

**Critérios de Aceitação:**
- ✅ Índices criados
- ✅ N+1 queries eliminados
- ✅ Connection pool configurado
- ✅ Queries <100ms em 95% dos casos

---

### **4.4 - Background Tasks com Celery**

**Dependências:**
```bash
celery==5.3.4
celery[redis]==5.3.4
flower==2.0.1  # Monitoring para Celery
```

**Tasks:**

1. [ ] **Setup Celery**
   ```python
   # app/celery_app.py
   from celery import Celery

   celery_app = Celery(
       "pizzaria",
       broker=os.getenv("REDIS_URL"),
       backend=os.getenv("REDIS_URL")
   )

   celery_app.conf.update(
       task_serializer="json",
       accept_content=["json"],
       result_serializer="json",
       timezone="America/Sao_Paulo",
       enable_utc=True,
   )
   ```

2. [ ] **Tasks assíncronas**
   ```python
   # app/tasks/email_tasks.py
   @celery_app.task
   def send_order_confirmation_email(order_id: int):
       # Buscar pedido
       # Renderizar template
       # Enviar email
       pass

   @celery_app.task
   def send_order_status_notification(order_id: int, new_status: str):
       pass
   ```

3. [ ] **Integrar com routers**
   ```python
   @router.post("/pedidos/")
   async def criar_pedido(...):
       # ... criar pedido ...

       # Enviar email em background
       send_order_confirmation_email.delay(pedido.id)

       return pedido
   ```

4. [ ] **Adicionar ao docker-compose**
   ```yaml
   celery-worker:
     build: ./backend
     command: celery -A app.celery_app worker --loglevel=info
     depends_on:
       - redis
       - postgres

   flower:
     build: ./backend
     command: celery -A app.celery_app flower
     ports:
       - "5555:5555"
     depends_on:
       - celery-worker
   ```

**Critérios de Aceitação:**
- ✅ Celery configurado
- ✅ Tasks de email funcionando
- ✅ Flower para monitoring
- ✅ Tasks não bloqueiam requests

---

### **✅ CHECKLIST FASE 4**

- [ ] Redis cache implementado
- [ ] Paginação em todas listagens
- [ ] Índices otimizados
- [ ] N+1 queries resolvidos
- [ ] Connection pooling configurado
- [ ] Celery para background tasks
- [ ] Performance targets atingidos (<200ms p95)

**Resultado Esperado:**
Sistema rápido, escalável, capaz de lidar com alto tráfego.

---

## **FASE 5: FUNCIONALIDADES PREMIUM**
**Objetivo:** Features de nível iFood/Rappi
**Duração:** 4-5 semanas
**Depende de:** Fases 1-4

### **5.1 - Sistema de Endereços**

**Tasks:**

1. [ ] **Criar modelo de Endereço**
   ```python
   class Endereco(Base):
       __tablename__ = "enderecos"

       id = Column(Integer, primary_key=True)
       usuario_id = Column(Integer, ForeignKey("usuarios.id"))
       tipo = Column(String)  # CASA, TRABALHO, OUTRO
       cep = Column(String(8), nullable=False)
       logradouro = Column(String, nullable=False)
       numero = Column(String, nullable=False)
       complemento = Column(String)
       bairro = Column(String, nullable=False)
       cidade = Column(String, nullable=False)
       estado = Column(String(2), nullable=False)
       referencia = Column(String)
       latitude = Column(Float)
       longitude = Column(Float)
       padrao = Column(Boolean, default=False)
       ativo = Column(Boolean, default=True)
       created_at = Column(DateTime, server_default=func.now())
   ```

2. [ ] **API de CEP (ViaCEP)**
   ```python
   # app/services/cep.py
   import httpx

   async def buscar_cep(cep: str) -> dict:
       async with httpx.AsyncClient() as client:
           response = await client.get(f"https://viacep.com.br/ws/{cep}/json/")
           return response.json()
   ```

3. [ ] **Endpoints de endereço**
   - POST /enderecos/ (criar)
   - GET /enderecos/ (listar meus)
   - PUT /enderecos/{id} (atualizar)
   - DELETE /enderecos/{id} (remover)
   - PATCH /enderecos/{id}/padrao (marcar como padrão)

4. [ ] **Adicionar endereço ao pedido**
   ```python
   class Pedido(Base):
       # ... campos existentes ...
       endereco_id = Column(Integer, ForeignKey("enderecos.id"))
       endereco = relationship("Endereco")
   ```

**Critérios de Aceitação:**
- ✅ CRUD completo de endereços
- ✅ Integração com ViaCEP
- ✅ Geocoding (lat/lng)
- ✅ Endereço padrão funcional

---

### **5.2 - Sistema de Pagamentos**

**Dependências:**
```bash
stripe==7.10.0
mercadopago==2.2.1
```

**Tasks:**

1. [ ] **Criar modelo de Pagamento**
   ```python
   class Pagamento(Base):
       __tablename__ = "pagamentos"

       id = Column(Integer, primary_key=True)
       pedido_id = Column(Integer, ForeignKey("pedidos.id"), unique=True)
       metodo = Column(String)  # CREDIT_CARD, DEBIT_CARD, PIX, DINHEIRO
       status = Column(String)  # PENDENTE, APROVADO, RECUSADO, CANCELADO
       valor = Column(Float, nullable=False)
       gateway_transaction_id = Column(String)
       gateway_response = Column(JSON)
       paid_at = Column(DateTime)
       created_at = Column(DateTime, server_default=func.now())
   ```

2. [ ] **Integração Stripe**
   ```python
   # app/services/stripe_service.py
   import stripe

   stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

   async def create_payment_intent(amount: float, order_id: int):
       intent = stripe.PaymentIntent.create(
           amount=int(amount * 100),  # Centavos
           currency="brl",
           metadata={"order_id": order_id}
       )
       return intent
   ```

3. [ ] **Integração Mercado Pago**
   ```python
   # app/services/mercadopago_service.py
   import mercadopago

   sdk = mercadopago.SDK(os.getenv("MERCADOPAGO_ACCESS_TOKEN"))

   async def create_pix_payment(amount: float, order_id: int):
       payment_data = {
           "transaction_amount": amount,
           "payment_method_id": "pix",
           "payer": {...}
       }
       payment = sdk.payment().create(payment_data)
       return payment
   ```

4. [ ] **Webhooks de pagamento**
   ```python
   @router.post("/webhooks/stripe")
   async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
       payload = await request.body()
       sig_header = request.headers.get("stripe-signature")

       event = stripe.Webhook.construct_event(
           payload, sig_header, STRIPE_WEBHOOK_SECRET
       )

       if event["type"] == "payment_intent.succeeded":
           # Atualizar status do pagamento
           # Atualizar status do pedido
           pass
   ```

5. [ ] **Endpoints**
   - POST /pagamentos/iniciar (criar payment intent)
   - GET /pagamentos/{pedido_id} (status)
   - POST /webhooks/stripe (webhook)
   - POST /webhooks/mercadopago (webhook)

**Critérios de Aceitação:**
- ✅ Stripe funcionando
- ✅ Mercado Pago funcionando
- ✅ PIX implementado
- ✅ Webhooks processando corretamente
- ✅ Status de pagamento sincronizado

---

### **5.3 - Sistema de Cupons e Descontos**

**Tasks:**

1. [ ] **Criar modelo de Cupom**
   ```python
   class Cupom(Base):
       __tablename__ = "cupons"

       id = Column(Integer, primary_key=True)
       codigo = Column(String, unique=True, index=True)
       tipo = Column(String)  # PERCENTUAL, VALOR_FIXO, FRETE_GRATIS
       valor = Column(Float)  # Percentual ou valor fixo
       valor_minimo_pedido = Column(Float)
       usos_maximos = Column(Integer)
       usos_por_usuario = Column(Integer, default=1)
       usos_realizados = Column(Integer, default=0)
       valido_de = Column(DateTime)
       valido_ate = Column(DateTime)
       ativo = Column(Boolean, default=True)
       created_at = Column(DateTime, server_default=func.now())
   ```

2. [ ] **Validação de cupom**
   ```python
   @router.post("/cupons/validar")
   async def validar_cupom(
       codigo: str,
       valor_pedido: float,
       user: Usuario = Depends(get_current_user),
       db: Session = Depends(get_db)
   ):
       cupom = db.query(Cupom).filter(Cupom.codigo == codigo).first()

       # Validações
       if not cupom or not cupom.ativo:
           raise CupomInvalidoException()

       if cupom.usos_maximos and cupom.usos_realizados >= cupom.usos_maximos:
           raise CupomEsgotadoException()

       if valor_pedido < cupom.valor_minimo_pedido:
           raise ValorMinimoPedidoException()

       # Calcular desconto
       desconto = calcular_desconto(cupom, valor_pedido)

       return {
           "valido": True,
           "desconto": desconto,
           "valor_final": valor_pedido - desconto
       }
   ```

3. [ ] **Aplicar cupom no pedido**
   ```python
   class Pedido(Base):
       # ... campos existentes ...
       cupom_id = Column(Integer, ForeignKey("cupons.id"))
       desconto = Column(Float, default=0.0)
       valor_final = Column(Float)  # preco_total - desconto
   ```

**Critérios de Aceitação:**
- ✅ CRUD de cupons (admin)
- ✅ Validação de cupom funcional
- ✅ Múltiplos tipos de desconto
- ✅ Limites de uso respeitados

---

### **5.4 - Sistema de Notificações**

**Dependências:**
```bash
firebase-admin==6.3.0  # Push notifications
twilio==8.11.1  # SMS/WhatsApp
```

**Tasks:**

1. [ ] **Criar modelo de Notificação**
   ```python
   class Notificacao(Base):
       __tablename__ = "notificacoes"

       id = Column(Integer, primary_key=True)
       usuario_id = Column(Integer, ForeignKey("usuarios.id"))
       tipo = Column(String)  # EMAIL, SMS, PUSH, WHATSAPP
       titulo = Column(String)
       mensagem = Column(Text)
       lida = Column(Boolean, default=False)
       enviada = Column(Boolean, default=False)
       enviada_em = Column(DateTime)
       created_at = Column(DateTime, server_default=func.now())
   ```

2. [ ] **Service de notificações**
   ```python
   # app/services/notification_service.py
   class NotificationService:
       async def send_order_status_notification(
           self,
           user: Usuario,
           order: Pedido,
           new_status: str
       ):
           # Email
           await self.send_email(...)

           # Push notification
           if user.fcm_token:
               await self.send_push(...)

           # SMS (opcional)
           if user.phone and user.sms_enabled:
               await self.send_sms(...)
   ```

3. [ ] **Push Notifications com Firebase**
   ```python
   # app/services/push_service.py
   import firebase_admin
   from firebase_admin import credentials, messaging

   cred = credentials.Certificate("firebase-credentials.json")
   firebase_admin.initialize_app(cred)

   async def send_push_notification(
       fcm_token: str,
       title: str,
       body: str,
       data: dict = None
   ):
       message = messaging.Message(
           notification=messaging.Notification(
               title=title,
               body=body
           ),
           data=data or {},
           token=fcm_token
       )

       response = messaging.send(message)
       return response
   ```

4. [ ] **Integração com routers**
   - Notificar ao criar pedido
   - Notificar ao mudar status
   - Notificar pagamento confirmado
   - Notificar entrega

**Critérios de Aceitação:**
- ✅ Email notifications funcionando
- ✅ Push notifications funcionando
- ✅ Histórico de notificações salvo
- ✅ Preferências de notificação por usuário

---

### **5.5 - Sistema de Avaliações**

**Tasks:**

1. [ ] **Criar modelo de Avaliação**
   ```python
   class Avaliacao(Base):
       __tablename__ = "avaliacoes"

       id = Column(Integer, primary_key=True)
       pedido_id = Column(Integer, ForeignKey("pedidos.id"), unique=True)
       usuario_id = Column(Integer, ForeignKey("usuarios.id"))
       nota = Column(Integer)  # 1-5
       comentario = Column(Text)
       resposta_admin = Column(Text)
       created_at = Column(DateTime, server_default=func.now())
   ```

2. [ ] **Endpoints**
   - POST /avaliacoes/ (criar)
   - GET /avaliacoes/ (listar - admin)
   - GET /avaliacoes/produto/{id} (média e reviews)
   - PATCH /avaliacoes/{id}/responder (admin responde)

3. [ ] **Calcular média de avaliações**
   ```python
   @router.get("/estatisticas/avaliacoes")
   async def estatisticas_avaliacoes(db: Session = Depends(get_db)):
       avg_nota = db.query(func.avg(Avaliacao.nota)).scalar()
       total = db.query(Avaliacao).count()

       distribuicao = db.query(
           Avaliacao.nota,
           func.count(Avaliacao.id)
       ).group_by(Avaliacao.nota).all()

       return {
           "media": avg_nota,
           "total": total,
           "distribuicao": dict(distribuicao)
       }
   ```

**Critérios de Aceitação:**
- ✅ Usuários podem avaliar pedidos entregues
- ✅ Média de avaliações calculada
- ✅ Admin pode responder avaliações

---

### **✅ CHECKLIST FASE 5**

- [ ] Sistema de endereços completo
- [ ] Integração com gateways de pagamento
- [ ] Sistema de cupons funcionando
- [ ] Notificações multi-canal (email, push, SMS)
- [ ] Sistema de avaliações implementado
- [ ] Testes de integração para novas features

**Resultado Esperado:**
Funcionalidades premium comparáveis a grandes apps de delivery.

---

## **FASE 6: FRONTEND PREMIUM** 🎨
**Objetivo:** Interface moderna e responsiva
**Duração:** 5-6 semanas
**Depende de:** Fase 5

### **6.1 - Setup do Projeto Frontend**

**Stack Escolhida:**
- **Framework:** Next.js 14 (React + SSR)
- **Linguagem:** TypeScript
- **Styling:** Tailwind CSS + shadcn/ui
- **State:** Zustand
- **Forms:** React Hook Form + Zod
- **HTTP:** Axios + React Query
- **Auth:** NextAuth.js

**Tasks:**

1. [ ] **Criar projeto Next.js**
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --app
   cd frontend
   ```

2. [ ] **Instalar dependências**
   ```bash
   npm install \
     @tanstack/react-query \
     axios \
     zustand \
     react-hook-form \
     zod \
     @hookform/resolvers \
     next-auth \
     date-fns \
     lucide-react \
     sonner  # Toasts

   # shadcn/ui
   npx shadcn-ui@latest init
   npx shadcn-ui@latest add button input card dialog form
   ```

3. [ ] **Estrutura de pastas**
   ```
   frontend/
   ├── app/
   │   ├── (auth)/
   │   │   ├── login/
   │   │   └── register/
   │   ├── (dashboard)/
   │   │   ├── pedidos/
   │   │   ├── cardapio/
   │   │   └── perfil/
   │   ├── (admin)/
   │   │   ├── dashboard/
   │   │   ├── produtos/
   │   │   ├── pedidos/
   │   │   └── usuarios/
   │   └── layout.tsx
   ├── components/
   │   ├── ui/         # shadcn components
   │   ├── forms/
   │   ├── cards/
   │   └── layouts/
   ├── lib/
   │   ├── api/        # API client
   │   ├── hooks/
   │   ├── utils/
   │   └── validations/
   ├── stores/
   │   ├── auth.ts
   │   └── cart.ts
   └── types/
       └── api.ts
   ```

4. [ ] **Configurar API client**
   ```typescript
   // lib/api/client.ts
   import axios from 'axios';

   export const api = axios.create({
     baseURL: process.env.NEXT_PUBLIC_API_URL,
   });

   api.interceptors.request.use((config) => {
     const token = localStorage.getItem('access_token');
     if (token) {
       config.headers.Authorization = `Bearer ${token}`;
     }
     return config;
   });

   api.interceptors.response.use(
     (response) => response,
     async (error) => {
       if (error.response?.status === 401) {
         // Tentar refresh token
         await refreshToken();
       }
       return Promise.reject(error);
     }
   );
   ```

**Critérios de Aceitação:**
- ✅ Projeto Next.js configurado
- ✅ Todas dependências instaladas
- ✅ Estrutura de pastas organizada
- ✅ API client configurado

---

### **6.2 - Autenticação Frontend**

**Tasks:**

1. [ ] **Auth store (Zustand)**
   ```typescript
   // stores/auth.ts
   import { create } from 'zustand';

   interface AuthState {
     user: User | null;
     token: string | null;
     login: (email: string, password: string) => Promise<void>;
     logout: () => void;
     isAuthenticated: () => boolean;
   }

   export const useAuth = create<AuthState>((set, get) => ({
     user: null,
     token: null,

     login: async (email, password) => {
       const response = await api.post('/auth/login', { email, password });
       const { access_token, user } = response.data;

       localStorage.setItem('access_token', access_token);
       set({ user, token: access_token });
     },

     logout: () => {
       localStorage.removeItem('access_token');
       set({ user: null, token: null });
     },

     isAuthenticated: () => !!get().token,
   }));
   ```

2. [ ] **Páginas de autenticação**
   - `/login` - Login form
   - `/register` - Registro
   - `/forgot-password` - Recuperação de senha
   - `/reset-password/[token]` - Reset senha

3. [ ] **Protected routes**
   ```typescript
   // components/ProtectedRoute.tsx
   export function ProtectedRoute({ children }: { children: React.ReactNode }) {
     const { isAuthenticated } = useAuth();
     const router = useRouter();

     useEffect(() => {
       if (!isAuthenticated()) {
         router.push('/login');
       }
     }, [isAuthenticated]);

     if (!isAuthenticated()) return null;

     return <>{children}</>;
   }
   ```

**Critérios de Aceitação:**
- ✅ Login funcional
- ✅ Registro funcional
- ✅ Logout funcional
- ✅ Protected routes funcionando
- ✅ Token refresh automático

---

### **6.3 - Cardápio e Carrinho**

**Tasks:**

1. [ ] **Página de Cardápio**
   ```tsx
   // app/(dashboard)/cardapio/page.tsx
   export default function CardapioPage() {
     const { data: produtos, isLoading } = useQuery({
       queryKey: ['produtos'],
       queryFn: () => api.get('/produtos').then(r => r.data)
     });

     return (
       <div className="container mx-auto py-8">
         <h1 className="text-3xl font-bold mb-8">Cardápio</h1>

         <Filters />

         <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
           {produtos?.map(produto => (
             <ProdutoCard
               key={produto.id}
               produto={produto}
               onAddToCart={addToCart}
             />
           ))}
         </div>
       </div>
     );
   }
   ```

2. [ ] **Componente ProdutoCard**
   ```tsx
   // components/ProdutoCard.tsx
   export function ProdutoCard({ produto, onAddToCart }) {
     return (
       <Card className="hover:shadow-lg transition-shadow">
         <CardContent className="p-6">
           <img
             src={produto.imagem || '/placeholder.png'}
             alt={produto.nome}
             className="w-full h-48 object-cover rounded-lg mb-4"
           />
           <h3 className="text-xl font-semibold">{produto.nome}</h3>
           <p className="text-gray-600 mt-2">{produto.descricao}</p>
           <div className="mt-4 flex items-center justify-between">
             <span className="text-2xl font-bold text-green-600">
               R$ {produto.preco.toFixed(2)}
             </span>
             <Button onClick={() => onAddToCart(produto)}>
               Adicionar
             </Button>
           </div>
         </CardContent>
       </Card>
     );
   }
   ```

3. [ ] **Carrinho de compras (Zustand)**
   ```typescript
   // stores/cart.ts
   interface CartItem {
     produto: Produto;
     quantidade: number;
     observacoes?: string;
   }

   interface CartState {
     items: CartItem[];
     addItem: (produto: Produto) => void;
     removeItem: (produtoId: number) => void;
     updateQuantidade: (produtoId: number, quantidade: number) => void;
     clear: () => void;
     total: () => number;
   }

   export const useCart = create<CartState>((set, get) => ({
     items: [],

     addItem: (produto) => {
       const items = get().items;
       const existing = items.find(i => i.produto.id === produto.id);

       if (existing) {
         set({
           items: items.map(i =>
             i.produto.id === produto.id
               ? { ...i, quantidade: i.quantidade + 1 }
               : i
           )
         });
       } else {
         set({ items: [...items, { produto, quantidade: 1 }] });
       }
     },

     removeItem: (produtoId) => {
       set({ items: get().items.filter(i => i.produto.id !== produtoId) });
     },

     updateQuantidade: (produtoId, quantidade) => {
       set({
         items: get().items.map(i =>
           i.produto.id === produtoId ? { ...i, quantidade } : i
         )
       });
     },

     clear: () => set({ items: [] }),

     total: () =>
       get().items.reduce(
         (sum, item) => sum + item.produto.preco * item.quantidade,
         0
       ),
   }));
   ```

4. [ ] **Sheet de Carrinho**
   ```tsx
   // components/CartSheet.tsx
   export function CartSheet() {
     const { items, total, removeItem } = useCart();

     return (
       <Sheet>
         <SheetTrigger>
           <Button variant="outline" className="relative">
             <ShoppingCart className="h-5 w-5" />
             {items.length > 0 && (
               <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs">
                 {items.length}
               </span>
             )}
           </Button>
         </SheetTrigger>

         <SheetContent>
           <SheetHeader>
             <SheetTitle>Seu Carrinho</SheetTitle>
           </SheetHeader>

           <div className="flex flex-col gap-4 py-4">
             {items.map(item => (
               <CartItem key={item.produto.id} item={item} />
             ))}
           </div>

           <div className="border-t pt-4">
             <div className="flex justify-between text-lg font-bold">
               <span>Total:</span>
               <span>R$ {total().toFixed(2)}</span>
             </div>

             <Button className="w-full mt-4" size="lg">
               Finalizar Pedido
             </Button>
           </div>
         </SheetContent>
       </Sheet>
     );
   }
   ```

**Critérios de Aceitação:**
- ✅ Listagem de produtos com filtros
- ✅ Adicionar ao carrinho funcional
- ✅ Carrinho persistente (localStorage)
- ✅ Cálculo de total correto

---

### **6.4 - Checkout e Pedidos**

**Tasks:**

1. [ ] **Página de Checkout**
   - Seleção de endereço
   - Revisão do pedido
   - Aplicar cupom
   - Seleção de pagamento
   - Confirmar pedido

2. [ ] **Página de Pedidos**
   ```tsx
   // app/(dashboard)/pedidos/page.tsx
   export default function PedidosPage() {
     const { data: pedidos } = useQuery({
       queryKey: ['meus-pedidos'],
       queryFn: () => api.get('/pedidos/meus').then(r => r.data)
     });

     return (
       <div className="container mx-auto py-8">
         <h1 className="text-3xl font-bold mb-8">Meus Pedidos</h1>

         <div className="space-y-4">
           {pedidos?.map(pedido => (
             <PedidoCard key={pedido.id} pedido={pedido} />
           ))}
         </div>
       </div>
     );
   }
   ```

3. [ ] **Tracking de Pedido em Tempo Real**
   ```tsx
   // components/PedidoTracking.tsx
   const STATUS_STEPS = [
     { key: 'PENDENTE', label: 'Pedido Recebido' },
     { key: 'EM_PREPARO', label: 'Preparando' },
     { key: 'PRONTO', label: 'Pronto' },
     { key: 'ENTREGUE', label: 'Entregue' }
   ];

   export function PedidoTracking({ status }) {
     const currentIndex = STATUS_STEPS.findIndex(s => s.key === status);

     return (
       <div className="flex items-center justify-between">
         {STATUS_STEPS.map((step, index) => (
           <div key={step.key} className="flex flex-col items-center">
             <div
               className={cn(
                 "w-10 h-10 rounded-full flex items-center justify-center",
                 index <= currentIndex
                   ? "bg-green-500 text-white"
                   : "bg-gray-200"
               )}
             >
               {index < currentIndex ? <Check /> : index + 1}
             </div>
             <span className="text-sm mt-2">{step.label}</span>
           </div>
         ))}
       </div>
     );
   }
   ```

**Critérios de Aceitação:**
- ✅ Checkout completo funcionando
- ✅ Listagem de pedidos
- ✅ Detalhes do pedido
- ✅ Tracking visual de status

---

### **6.5 - Painel Administrativo**

**Tasks:**

1. [ ] **Dashboard com KPIs**
   ```tsx
   // app/(admin)/dashboard/page.tsx
   export default function AdminDashboard() {
     const { data: stats } = useQuery({
       queryKey: ['admin-stats'],
       queryFn: () => api.get('/metrics').then(r => r.data)
     });

     return (
       <div className="container mx-auto py-8">
         <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

         <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
           <StatsCard
             title="Pedidos Hoje"
             value={stats?.pedidos_hoje}
             icon={<ShoppingBag />}
           />
           <StatsCard
             title="Faturamento"
             value={`R$ ${stats?.faturamento_hoje}`}
             icon={<DollarSign />}
           />
           <StatsCard
             title="Novos Usuários"
             value={stats?.usuarios_novos}
             icon={<Users />}
           />
           <StatsCard
             title="Ticket Médio"
             value={`R$ ${stats?.ticket_medio}`}
             icon={<TrendingUp />}
           />
         </div>

         <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
           <Card>
             <CardHeader>
               <CardTitle>Pedidos Recentes</CardTitle>
             </CardHeader>
             <CardContent>
               <RecentOrdersTable />
             </CardContent>
           </Card>

           <Card>
             <CardHeader>
               <CardTitle>Gráfico de Vendas</CardTitle>
             </CardHeader>
             <CardContent>
               <SalesChart data={stats?.vendas_7dias} />
             </CardContent>
           </Card>
         </div>
       </div>
     );
   }
   ```

2. [ ] **Gestão de Produtos**
   - Listagem com DataTable
   - Criar/Editar produto (Dialog)
   - Upload de imagem
   - Ativar/Desativar

3. [ ] **Gestão de Pedidos**
   - Listagem em tempo real
   - Filtros (status, data)
   - Atualizar status
   - Ver detalhes

4. [ ] **Gestão de Usuários**
   - Listagem
   - Ativar/Desativar
   - Tornar admin

**Critérios de Aceitação:**
- ✅ Dashboard com métricas em tempo real
- ✅ CRUD completo de produtos
- ✅ Gestão de pedidos funcional
- ✅ Gestão de usuários funcional

---

### **6.6 - PWA e Otimizações**

**Tasks:**

1. [ ] **Configurar PWA**
   ```javascript
   // next.config.js
   const withPWA = require('next-pwa')({
     dest: 'public',
     register: true,
     skipWaiting: true,
   });

   module.exports = withPWA({
     // ... outras configs
   });
   ```

2. [ ] **Manifest.json**
   ```json
   {
     "name": "Pizzaria App",
     "short_name": "Pizzaria",
     "icons": [...],
     "theme_color": "#FF6B35",
     "background_color": "#FFFFFF",
     "display": "standalone",
     "start_url": "/"
   }
   ```

3. [ ] **Otimizações**
   - Image optimization (next/image)
   - Code splitting
   - Lazy loading
   - Font optimization
   - SEO metadata

**Critérios de Aceitação:**
- ✅ PWA instalável
- ✅ Offline support básico
- ✅ Performance score >90 (Lighthouse)
- ✅ SEO score >90

---

### **6.7 - Testes E2E**

**Dependências:**
```bash
npm install -D @playwright/test
npx playwright install
```

**Tasks:**

1. [ ] **Setup Playwright**
   ```typescript
   // playwright.config.ts
   export default defineConfig({
     testDir: './e2e',
     use: {
       baseURL: 'http://localhost:3000',
     },
     webServer: {
       command: 'npm run dev',
       port: 3000,
     },
   });
   ```

2. [ ] **Testes principais**
   ```typescript
   // e2e/auth.spec.ts
   test('should login successfully', async ({ page }) => {
     await page.goto('/login');
     await page.fill('[name="email"]', 'user@example.com');
     await page.fill('[name="password"]', 'password123');
     await page.click('button[type="submit"]');

     await expect(page).toHaveURL('/dashboard');
   });

   // e2e/order.spec.ts
   test('should create order', async ({ page }) => {
     // Login
     // Navegar para cardápio
     // Adicionar produtos ao carrinho
     // Finalizar pedido
     // Verificar criação
   });
   ```

**Critérios de Aceitação:**
- ✅ Testes de autenticação
- ✅ Testes de criação de pedido
- ✅ Testes de admin
- ✅ Coverage >70%

---

### **6.8 - Dockerfile Frontend**

**Tasks:**

1. [ ] **Criar Dockerfile**
   ```dockerfile
   # frontend/Dockerfile
   FROM node:20-alpine AS builder
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci
   COPY . .
   RUN npm run build

   FROM node:20-alpine AS runner
   WORKDIR /app
   ENV NODE_ENV production

   COPY --from=builder /app/public ./public
   COPY --from=builder /app/.next/standalone ./
   COPY --from=builder /app/.next/static ./.next/static

   EXPOSE 3000
   CMD ["node", "server.js"]
   ```

2. [ ] **Atualizar docker-compose**
   ```yaml
   frontend:
     build:
       context: ./frontend
       dockerfile: Dockerfile
     container_name: pizzaria-frontend
     environment:
       NEXT_PUBLIC_API_URL: http://backend:8000
     ports:
       - "3000:3000"
     depends_on:
       - backend
   ```

**Critérios de Aceitação:**
- ✅ Frontend rodando em Docker
- ✅ Comunicação com backend funcionando

---

### **✅ CHECKLIST FASE 6**

- [ ] Next.js configurado com TypeScript
- [ ] Autenticação frontend completa
- [ ] Cardápio e carrinho funcionais
- [ ] Checkout e pedidos implementados
- [ ] Painel admin completo
- [ ] PWA configurado
- [ ] Testes E2E implementados
- [ ] Dockerfile frontend criado
- [ ] Design responsivo (mobile-first)
- [ ] Performance otimizada

**Resultado Esperado:**
Frontend premium, rápido, responsivo, com UX comparável a grandes apps.

---

## **FASE 7: INFRAESTRUTURA AVANÇADA**
**Objetivo:** Deploy production-ready
**Duração:** 2-3 semanas
**Depende de:** Fases 1-6

### **7.1 - CI/CD com GitHub Actions**

**Tasks:**

1. [ ] **Criar workflow de CI**
   ```yaml
   # .github/workflows/ci.yml
   name: CI

   on:
     push:
       branches: [main, develop]
     pull_request:
       branches: [main, develop]

   jobs:
     backend-tests:
       runs-on: ubuntu-latest

       services:
         postgres:
           image: postgres:15
           env:
             POSTGRES_PASSWORD: postgres
           options: >-
             --health-cmd pg_isready
             --health-interval 10s
             --health-timeout 5s
             --health-retries 5

       steps:
         - uses: actions/checkout@v4

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: |
             cd backend
             pip install -r requirements.txt

         - name: Run linters
           run: |
             black --check backend/app
             ruff check backend/app

         - name: Run tests
           run: |
             cd backend
             pytest tests/ -v --cov=app --cov-report=xml

         - name: Upload coverage
           uses: codecov/codecov-action@v3
           with:
             file: ./backend/coverage.xml

     frontend-tests:
       runs-on: ubuntu-latest

       steps:
         - uses: actions/checkout@v4

         - name: Set up Node
           uses: actions/setup-node@v4
           with:
             node-version: '20'

         - name: Install dependencies
           run: |
             cd frontend
             npm ci

         - name: Run linters
           run: |
             cd frontend
             npm run lint

         - name: Run tests
           run: |
             cd frontend
             npm run test

         - name: Run E2E tests
           run: |
             cd frontend
             npx playwright test

     security-scan:
       runs-on: ubuntu-latest

       steps:
         - uses: actions/checkout@v4

         - name: Run Trivy vulnerability scanner
           uses: aquasecurity/trivy-action@master
           with:
             scan-type: 'fs'
             scan-ref: '.'
             format: 'sarif'
             output: 'trivy-results.sarif'

         - name: Upload Trivy results to GitHub Security tab
           uses: github/codeql-action/upload-sarif@v2
           with:
             sarif_file: 'trivy-results.sarif'
   ```

2. [ ] **Criar workflow de CD**
   ```yaml
   # .github/workflows/cd.yml
   name: CD

   on:
     push:
       branches: [main]
       tags:
         - 'v*'

   jobs:
     build-and-push:
       runs-on: ubuntu-latest

       steps:
         - uses: actions/checkout@v4

         - name: Set up Docker Buildx
           uses: docker/setup-buildx-action@v3

         - name: Login to Docker Hub
           uses: docker/login-action@v3
           with:
             username: ${{ secrets.DOCKER_USERNAME }}
             password: ${{ secrets.DOCKER_PASSWORD }}

         - name: Build and push backend
           uses: docker/build-push-action@v5
           with:
             context: ./backend
             push: true
             tags: |
               ${{ secrets.DOCKER_USERNAME }}/pizzaria-backend:latest
               ${{ secrets.DOCKER_USERNAME }}/pizzaria-backend:${{ github.sha }}

         - name: Build and push frontend
           uses: docker/build-push-action@v5
           with:
             context: ./frontend
             push: true
             tags: |
               ${{ secrets.DOCKER_USERNAME }}/pizzaria-frontend:latest
               ${{ secrets.DOCKER_USERNAME }}/pizzaria-frontend:${{ github.sha }}

     deploy:
       needs: build-and-push
       runs-on: ubuntu-latest

       steps:
         - name: Deploy to production
           uses: appleboy/ssh-action@master
           with:
             host: ${{ secrets.PROD_HOST }}
             username: ${{ secrets.PROD_USER }}
             key: ${{ secrets.SSH_PRIVATE_KEY }}
             script: |
               cd /app/pizzaria
               docker-compose pull
               docker-compose up -d
               docker system prune -f
   ```

**Critérios de Aceitação:**
- ✅ CI rodando em todos PRs
- ✅ Tests obrigatórios para merge
- ✅ Deploy automático em main
- ✅ Security scanning ativo

---

### **7.2 - Kubernetes (Opcional - para escala alta)**

**Tasks:**

1. [ ] **Criar manifests Kubernetes**
   ```yaml
   # k8s/backend-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: pizzaria-backend
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: pizzaria-backend
     template:
       metadata:
         labels:
           app: pizzaria-backend
       spec:
         containers:
         - name: backend
           image: pizzaria-backend:latest
           ports:
           - containerPort: 8000
           env:
           - name: DATABASE_URL
             valueFrom:
               secretKeyRef:
                 name: pizzaria-secrets
                 key: database-url
           livenessProbe:
             httpGet:
               path: /health
               port: 8000
             initialDelaySeconds: 30
             periodSeconds: 10
           resources:
             requests:
               memory: "256Mi"
               cpu: "250m"
             limits:
               memory: "512Mi"
               cpu: "500m"
   ```

2. [ ] **Horizontal Pod Autoscaler**
   ```yaml
   # k8s/backend-hpa.yaml
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: pizzaria-backend-hpa
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: pizzaria-backend
     minReplicas: 2
     maxReplicas: 10
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
   ```

3. [ ] **Ingress**
   ```yaml
   # k8s/ingress.yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: pizzaria-ingress
     annotations:
       cert-manager.io/cluster-issuer: "letsencrypt-prod"
   spec:
     tls:
     - hosts:
       - api.pizzaria.com
       secretName: pizzaria-tls
     rules:
     - host: api.pizzaria.com
       http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: pizzaria-backend
               port:
                 number: 8000
   ```

**Critérios de Aceitação:**
- ✅ Pods rodando em cluster
- ✅ Auto-scaling funcionando
- ✅ HTTPS configurado
- ✅ Health checks ativos

---

### **7.3 - Backup e Disaster Recovery**

**Tasks:**

1. [ ] **Backup automático de PostgreSQL**
   ```bash
   # scripts/backup.sh
   #!/bin/bash

   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   BACKUP_DIR="/backups"

   # Backup PostgreSQL
   pg_dump $DATABASE_URL > $BACKUP_DIR/backup_$TIMESTAMP.sql

   # Comprimir
   gzip $BACKUP_DIR/backup_$TIMESTAMP.sql

   # Upload para S3
   aws s3 cp $BACKUP_DIR/backup_$TIMESTAMP.sql.gz \
     s3://pizzaria-backups/database/

   # Deletar backups locais antigos (>7 dias)
   find $BACKUP_DIR -type f -mtime +7 -delete
   ```

2. [ ] **Cronjob para backups**
   ```yaml
   # k8s/backup-cronjob.yaml
   apiVersion: batch/v1
   kind: CronJob
   metadata:
     name: database-backup
   spec:
     schedule: "0 2 * * *"  # 2 AM todo dia
     jobTemplate:
       spec:
         template:
           spec:
             containers:
             - name: backup
               image: postgres:15
               command: ["/backup.sh"]
               volumeMounts:
               - name: backup-script
                 mountPath: /backup.sh
                 subPath: backup.sh
   ```

3. [ ] **Plano de recovery**
   ```bash
   # scripts/restore.sh
   #!/bin/bash

   BACKUP_FILE=$1

   # Download do S3
   aws s3 cp s3://pizzaria-backups/database/$BACKUP_FILE .

   # Descomprimir
   gunzip $BACKUP_FILE

   # Restore
   psql $DATABASE_URL < ${BACKUP_FILE%.gz}
   ```

**Critérios de Aceitação:**
- ✅ Backups diários automáticos
- ✅ Backups armazenados em S3
- ✅ Restore testado
- ✅ Documentação de DR

---

### **✅ CHECKLIST FASE 7**

- [ ] CI/CD pipeline funcionando
- [ ] Deploy automatizado
- [ ] Kubernetes configurado (se aplicável)
- [ ] Backup automático
- [ ] Disaster recovery plan documentado
- [ ] Monitoring em produção
- [ ] Alertas configurados

**Resultado Esperado:**
Sistema production-ready, resiliente, com deploy automatizado.

---

## **FASE 8: FEATURES AVANÇADAS (OPCIONAL)**
**Objetivo:** Diferenciais competitivos
**Duração:** 3-4 semanas
**Depende de:** Fases anteriores

### **8.1 - Sistema de Recomendações**

**Dependências:**
```bash
scikit-learn==1.3.2
pandas==2.1.4
```

**Tasks:**

1. [ ] **Modelo de recomendação colaborativa**
   ```python
   # app/ml/recommendations.py
   from sklearn.metrics.pairwise import cosine_similarity
   import pandas as pd

   def get_recommendations(user_id: int, db: Session) -> List[Produto]:
       # Buscar histórico de pedidos
       pedidos = db.query(Pedido).join(ItemPedido).all()

       # Criar matriz user-item
       user_item_matrix = create_user_item_matrix(pedidos)

       # Calcular similaridade
       similarity = cosine_similarity(user_item_matrix)

       # Recomendar produtos
       recommendations = get_top_recommendations(user_id, similarity)

       return recommendations
   ```

2. [ ] **Endpoint de recomendações**
   ```python
   @router.get("/recomendacoes/")
   async def recomendacoes(
       user: Usuario = Depends(get_current_user),
       db: Session = Depends(get_db)
   ):
       produtos = get_recommendations(user.id, db)
       return produtos
   ```

**Critérios de Aceitação:**
- ✅ Recomendações baseadas em histórico
- ✅ Performance aceitável (<500ms)
- ✅ Fallback para produtos populares

---

### **8.2 - Chat em Tempo Real (Suporte)**

**Dependências:**
```bash
fastapi-socketio==0.0.10
```

**Tasks:**

1. [ ] **WebSocket para chat**
   ```python
   # app/websockets/chat.py
   from fastapi import WebSocket
   from typing import List

   class ConnectionManager:
       def __init__(self):
           self.active_connections: List[WebSocket] = []

       async def connect(self, websocket: WebSocket):
           await websocket.accept()
           self.active_connections.append(websocket)

       async def broadcast(self, message: str):
           for connection in self.active_connections:
               await connection.send_text(message)

   manager = ConnectionManager()

   @app.websocket("/ws/chat/{user_id}")
   async def chat(websocket: WebSocket, user_id: int):
       await manager.connect(websocket)
       try:
           while True:
               data = await websocket.receive_text()
               await manager.broadcast(f"User {user_id}: {data}")
       except WebSocketDisconnect:
           manager.disconnect(websocket)
   ```

2. [ ] **Frontend chat component**
   - Socket.io client
   - Chat UI com mensagens
   - Notificações de novas mensagens

**Critérios de Aceitação:**
- ✅ Chat em tempo real funcional
- ✅ Admin pode responder
- ✅ Histórico de mensagens salvo

---

### **8.3 - Analytics Dashboard**

**Tasks:**

1. [ ] **Endpoints de analytics**
   ```python
   @router.get("/analytics/vendas")
   async def analytics_vendas(
       periodo: str,  # hoje, semana, mes, ano
       admin: Usuario = Depends(require_admin),
       db: Session = Depends(get_db)
   ):
       # Vendas por período
       # Produtos mais vendidos
       # Horários de pico
       # Taxa de conversão
       return analytics_data
   ```

2. [ ] **Gráficos interativos**
   - Recharts / Chart.js
   - Vendas por período
   - Produtos mais vendidos
   - Mapa de calor (horários)

**Critérios de Aceitação:**
- ✅ Dashboard com métricas relevantes
- ✅ Filtros por período
- ✅ Exportação de relatórios

---

### **8.4 - Programa de Fidelidade**

**Tasks:**

1. [ ] **Modelo de Pontos**
   ```python
   class PontosFidelidade(Base):
       __tablename__ = "pontos_fidelidade"

       id = Column(Integer, primary_key=True)
       usuario_id = Column(Integer, ForeignKey("usuarios.id"))
       pontos = Column(Integer, default=0)
       nivel = Column(String)  # BRONZE, PRATA, OURO, PLATINA
       created_at = Column(DateTime, server_default=func.now())
       updated_at = Column(DateTime, onupdate=func.now())

   class HistoricoPontos(Base):
       __tablename__ = "historico_pontos"

       id = Column(Integer, primary_key=True)
       usuario_id = Column(Integer, ForeignKey("usuarios.id"))
       pontos = Column(Integer)
       motivo = Column(String)
       pedido_id = Column(Integer, ForeignKey("pedidos.id"))
       created_at = Column(DateTime, server_default=func.now())
   ```

2. [ ] **Sistema de pontos**
   - Ganhar pontos ao fazer pedido
   - Níveis com benefícios
   - Trocar pontos por descontos
   - Expiração de pontos

**Critérios de Aceitação:**
- ✅ Pontos acumulados corretamente
- ✅ Níveis funcionando
- ✅ Resgate de pontos funcional

---

### **✅ CHECKLIST FASE 8**

- [ ] Sistema de recomendações ativo
- [ ] Chat em tempo real funcional
- [ ] Analytics dashboard implementado
- [ ] Programa de fidelidade funcionando

**Resultado Esperado:**
Diferenciais competitivos que aumentam engajamento e retenção.

---

## 🎯 REORGANIZAÇÃO DE ARQUITETURA

### **Estrutura Final Proposta**

```
pizzaria-enterprise/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── error_handlers.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── routers/
│   │   │       │   ├── auth.py
│   │   │       │   ├── orders.py
│   │   │       │   ├── products.py
│   │   │       │   ├── users.py
│   │   │       │   ├── payments.py
│   │   │       │   └── health.py
│   │   │       └── __init__.py
│   │   ├── core/
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   └── cache.py
│   │   ├── middleware/
│   │   │   ├── cors.py
│   │   │   ├── rate_limit.py
│   │   │   ├── correlation_id.py
│   │   │   └── security_headers.py
│   │   ├── models/
│   │   │   └── models.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── order.py
│   │   │   ├── product.py
│   │   │   ├── payment.py
│   │   │   └── pagination.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── order_service.py
│   │   │   ├── payment_service.py
│   │   │   ├── email_service.py
│   │   │   ├── notification_service.py
│   │   │   └── cep_service.py
│   │   ├── tasks/
│   │   │   ├── celery_app.py
│   │   │   ├── email_tasks.py
│   │   │   └── notification_tasks.py
│   │   └── utils/
│   │       ├── password.py
│   │       └── validators.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── factories.py
│   │   ├── unit/
│   │   └── integration/
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   ├── scripts/
│   │   ├── seed.py
│   │   ├── backup.sh
│   │   └── restore.sh
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pytest.ini
│   ├── pyproject.toml
│   ├── .flake8
│   ├── .env.example
│   └── README.md
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── stores/
│   ├── types/
│   ├── e2e/
│   ├── public/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── playwright.config.ts
│   └── README.md
├── k8s/
│   ├── backend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── hpa.yaml
│   ├── frontend/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── postgres/
│   │   ├── statefulset.yaml
│   │   └── service.yaml
│   ├── redis/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── ingress.yaml
│   ├── secrets.yaml
│   └── configmap.yaml
├── docs/
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── database-schema.png
│   │   └── component-diagram.png
│   ├── api/
│   │   ├── postman-collection.json
│   │   └── insomnia-workspace.json
│   ├── deployment/
│   │   ├── docker.md
│   │   └── kubernetes.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── CONTRIBUTING.md
│   └── SECURITY.md
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── Makefile
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
├── CHANGELOG.md
├── CLAUDE.md
└── melhorias.md  # Este arquivo
```

---

## 📈 MÉTRICAS DE SUCESSO

### **Performance**
- [ ] Response time p95 < 200ms
- [ ] Response time p99 < 500ms
- [ ] Availability > 99.9%
- [ ] Error rate < 0.1%

### **Qualidade**
- [ ] Test coverage ≥ 85%
- [ ] Zero critical security issues
- [ ] Code quality score > 8/10
- [ ] Tech debt < 10%

### **DevOps**
- [ ] Deploy frequency: > 5/semana
- [ ] Lead time for changes: < 1 dia
- [ ] MTTR (Mean Time to Recovery): < 1 hora
- [ ] Change failure rate: < 5%

### **Frontend**
- [ ] Lighthouse Performance: > 90
- [ ] Lighthouse Accessibility: > 95
- [ ] Lighthouse Best Practices: > 95
- [ ] Lighthouse SEO: > 90
- [ ] First Contentful Paint: < 1.5s
- [ ] Time to Interactive: < 3s

### **Business**
- [ ] Taxa de conversão: > 5%
- [ ] Taxa de retenção: > 60%
- [ ] NPS: > 50
- [ ] Ticket médio: crescimento de 20%

---

## 🚀 PRÓXIMOS PASSOS IMEDIATOS

### **Semana 1-2: Fundação Crítica**
1. ✅ Implementar testes (Fase 1.1)
2. ✅ Configurar Docker (Fase 1.2)
3. ✅ Setup Alembic + PostgreSQL (Fase 1.3)
4. ✅ Configurar linters (Fase 1.4)

### **Semana 3-4: Segurança**
1. ✅ Corrigir vulnerabilidades críticas (Fase 2.1)
2. ✅ Implementar autenticação avançada (Fase 2.2)
3. ✅ Audit logging (Fase 2.3)

### **Semana 5-6: Observabilidade**
1. ✅ Logging estruturado (Fase 3.1)
2. ✅ Sentry (Fase 3.2)
3. ✅ Prometheus + Grafana (Fase 3.3)

### **Semana 7-8: Performance**
1. ✅ Cache Redis (Fase 4.1)
2. ✅ Paginação (Fase 4.2)
3. ✅ Otimização de queries (Fase 4.3)
4. ✅ Celery (Fase 4.4)

### **Semana 9+: Features e Frontend**
1. ✅ Implementar features premium (Fase 5)
2. ✅ Desenvolver frontend (Fase 6)
3. ✅ CI/CD (Fase 7)

---

## 💰 ESTIMATIVA DE CUSTOS (Infraestrutura)

### **Development**
- Local (Docker Compose): R$ 0/mês

### **Staging**
- VPS (4GB RAM, 2 CPU): R$ 80/mês
- PostgreSQL (managed): R$ 50/mês
- Redis (managed): R$ 30/mês
- **Total: ~R$ 160/mês**

### **Production (Médio Porte)**
- Kubernetes cluster (3 nodes): R$ 400/mês
- PostgreSQL (managed, HA): R$ 200/mês
- Redis (managed, HA): R$ 100/mês
- S3 storage: R$ 30/mês
- CloudFlare CDN: R$ 50/mês
- Sentry: R$ 50/mês (plano team)
- Grafana Cloud: R$ 0 (free tier)
- SendGrid (emails): R$ 30/mês
- Twilio (SMS): R$ 100/mês (variável)
- **Total: ~R$ 960/mês**

### **Production (Alto Tráfego)**
- Auto-scaling cluster: R$ 1.500/mês
- Multi-AZ database: R$ 500/mês
- Redis cluster: R$ 300/mês
- CDN + Storage: R$ 200/mês
- Monitoring stack: R$ 150/mês
- **Total: ~R$ 2.650/mês**

---

## 📚 RECURSOS E REFERÊNCIAS

### **Documentação**
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Docker Docs](https://docs.docker.com/)
- [Kubernetes Docs](https://kubernetes.io/docs/)

### **Cursos Recomendados**
- FastAPI Best Practices (testdriven.io)
- Next.js Pro (Lee Robinson)
- AWS/GCP/Azure Certification
- Docker & Kubernetes Masterclass

### **Ferramentas**
- Postman / Insomnia (API testing)
- DBeaver (Database management)
- Grafana (Monitoring)
- Sentry (Error tracking)
- GitHub Actions (CI/CD)

---

## ✅ CONCLUSÃO

Este plano transforma o projeto atual (34% enterprise-ready) em um sistema de nível **premium/enterprise (95%+ ready)** comparável a grandes plataformas de delivery.

**Principais Conquistas ao Final:**
- ✅ Código testado e confiável (>85% coverage)
- ✅ Segurança enterprise-grade
- ✅ Performance otimizada (<200ms p95)
- ✅ Deploy automatizado (CI/CD)
- ✅ Observabilidade completa
- ✅ Frontend premium (Next.js + TypeScript)
- ✅ Escalabilidade horizontal
- ✅ Backup e disaster recovery
- ✅ Features avançadas (pagamentos, notificações, fidelidade)

**Timeline Total:** 9-13 meses (1-2 devs full-time)
**Investimento Total:** R$ 200-300k (desenvolvimento) + R$ 1-3k/mês (infraestrutura)

---

**Próximo Passo:** Começar pela **Fase 1** imediatamente! 🚀
