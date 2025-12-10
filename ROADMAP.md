# ROADMAP DE DESENVOLVIMENTO - Sistema de Pizzaria

Plano de implementacao incremental para evoluir o sistema a um nivel comparavel a plataformas como iFood, Rappi e Uber Eats.

**Versao:** 2.0  
**Data:** 03/12/2025  
**Abordagem:** Backend -> Testes -> Frontend (incremental por funcionalidade)

---

## O QUE JA ESTA IMPLEMENTADO

### Backend
- Autenticacao JWT completa (access + refresh tokens)
- CRUD de Usuarios com roles (admin/user) e enderecos
- Sistema de Categorias (CRUD admin + listagem publica ordenada)
- Sistema de Ingredientes (CRUD admin + controle de disponibilidade)
- CRUD de Produtos com Variacoes (multiplos tamanhos/precos por produto)
- Ingredientes Padrao (muitos-para-muitos com flag obrigatorio)
- Cardapio Publico dinamico (otimizado com eager loading)
- CRUD de Pedidos com customizacoes (adicionar/remover ingredientes)
- Calculo automatico de precos (base + ingredientes × quantidade)
- Sistema de permissoes e ownership
- Tratamento de erros robusto (14 excecoes customizadas + 5 handlers)
- Health checks e endpoints de monitoramento
- Validacao Pydantic v2
- Script de seed data completo
- Soft Delete e Timestamp Mixins

### Testes
- 101 testes (69 passando, 32 precisam correcao)
- Cobertura de 77% (meta: 80%+)
- Fixtures e factories configurados
- Testes unitarios completos para models e schemas

### Infraestrutura
- SQLite (migracao para PostgreSQL planejada)
- Estrutura de routers, models, schemas organizada
- Documentacao Swagger/ReDoc automatica

---

## FASE 1: FUNDACAO SOLIDA

### 1.1 Corrigir Base de Testes Existente [CONCLUIDO]

**Concluido em:** 06/12/2025  
**Resultado:** 97/97 testes passando | Cobertura 93% | Tempo 28.7s

### 1.2 Aprimorar Modelos de Dados [CONCLUIDO]

**Concluido em:** 06/12/2025  
**Resultado:** 108/108 testes passando | Cobertura 93.54% | Mixins + Endereco + 12 novos testes

### 1.3 Sistema de Categorias e Cardapio Dinamico [CONCLUIDO]

**Concluido em:** 10/12/2025
**Resultado:** Backend completo | 4 novos modelos | 5 routers | Seed data funcional

**Backend** ✅
- ✅ Criar modelo Categoria (nome, descricao, icone, ordem_exibicao, ativa)
- ✅ Criar modelo Ingrediente (nome, preco_adicional, disponivel)
- ✅ Criar modelo ProdutoVariacao (produto_id, tamanho, preco, disponivel)
- ✅ Criar modelo ProdutoIngrediente (muitos-para-muitos com flag obrigatorio)
- ✅ Refatorar Produto para usar FK para Categoria + variacoes
- ✅ Refatorar ItemPedido para suportar customizacoes (JSON)
- ✅ Router de Categorias (CRUD admin + listagem publica)
- ✅ Router de Ingredientes (CRUD admin + listagem publica)
- ✅ Router de Produtos refatorado (variacoes + ingredientes padrao)
- ✅ Router de Cardapio publico (otimizado com joinedload)
- ✅ Router de Pedidos refatorado (customizacoes + calculo de preco)
- ✅ Sistema de customizacao de pizza (adicionar/remover ingredientes)
- ✅ Validacoes de negocio (ingredientes obrigatorios, disponibilidade)
- ✅ Script de seed data (3 categorias + 15 ingredientes + 10 produtos)
- ✅ 6 novas excecoes customizadas
- ✅ Documentacao atualizada (README.md com breaking changes)

**Testes** ⏳
- ⏳ Testes de criacao e atualizacao de categorias
- ⏳ Testes de listagem de cardapio com filtros
- ⏳ Testes de validacao de ingredientes
- ⏳ Testes de customizacao de produtos

**Frontend** 📋
- 📋 Tela de cardapio com navegacao por categorias
- 📋 Cards de produtos com imagem, nome, descricao, preco
- 📋 Modal de detalhes do produto
- 📋 Interface de customizacao de pizza (checkboxes de ingredientes)
- 📋 Carrinho de compras (sidebar ou modal)
- 📋 Badge de quantidade de itens no carrinho

**Observacoes:**
- Banco de dados precisa ser recriado (breaking changes)
- Estrutura pronta para escalar com mais categorias e produtos
- Sistema de precificacao dinamica implementado
- Eager loading configurado para evitar N+1 queries

### 1.4 Sistema de Enderecos Completo

**Backend**
- CRUD completo de enderecos do usuario
- Validacao de CEP (integracao com API ViaCEP)
- Marcacao de endereco padrao
- Calculo de taxa de entrega por regiao/bairro
- Criar modelo TaxaEntrega (bairro, cidade, valor, tempo_estimado)

**Testes**
- Testes de CRUD de enderecos
- Testes de validacao de CEP
- Testes de calculo de taxa de entrega
- Testes de permissoes (usuario so ve seus enderecos)

**Frontend**
- Tela de gerenciamento de enderecos
- Formulario de cadastro com busca automatica por CEP
- Selecao de endereco de entrega no checkout
- Exibicao de taxa de entrega e tempo estimado

---

## FASE 2: SEGURANCA E AUTENTICACAO AVANCADA

### 2.1 Fortificacao de Seguranca

**Backend**
- Configurar CORS com origens especificas (variavel de ambiente)
- Implementar rate limiting em endpoints sensiveis (login, registro, reset password)
- Criar middleware de security headers (X-Frame-Options, CSP, HSTS, etc.)
- Validacao de forca de senha (minimo 8 caracteres, maiuscula, minuscula, numero, especial)
- Geracao de SECRET_KEY forte (512 bits)
- Implementar account lockout apos N tentativas de login falhadas
- Sistema de token blacklist com Redis (logout efetivo)

**Testes**
- Testes de rate limiting
- Testes de validacao de senha forte
- Testes de lockout de conta
- Testes de logout com invalidacao de token

**Frontend**
- Indicador de forca de senha em tempo real
- Mensagens de erro claras para tentativas de login bloqueadas
- Confirmacao visual de logout bem-sucedido

### 2.2 Sistema de Recuperacao de Senha

**Backend**
- Endpoint de forgot password (geracao de token temporario)
- Endpoint de reset password (validacao de token + atualizacao de senha)
- Endpoint de change password (usuario autenticado)
- Envio de emails transacionais (configuracao SMTP)
- Templates HTML de email profissionais (reset password, confirmacao)
- Tokens temporarios com expiracao (1 hora)

**Testes**
- Testes de fluxo completo de recuperacao de senha
- Testes de expiracao de tokens
- Testes de validacao de token invalido
- Mock de envio de emails

**Frontend**
- Tela de "Esqueci minha senha"
- Tela de redefinicao de senha (com token na URL)
- Tela de alteracao de senha (usuario logado)
- Feedback visual de sucesso/erro

### 2.3 Verificacao de Email

**Backend**
- Adicionar campo email_verified ao modelo Usuario
- Gerar token de verificacao no registro
- Endpoint de verify email
- Endpoint de resend verification email
- Bloquear certas acoes para usuarios nao verificados

**Testes**
- Testes de fluxo de verificacao de email
- Testes de reenvio de email
- Testes de permissoes para usuarios nao verificados

**Frontend**
- Banner de aviso para usuario nao verificado
- Botao de reenviar email de verificacao
- Tela de confirmacao de verificacao

### 2.4 Audit Logging

**Backend**
- Criar modelo AuditLog (user_id, action, entity_type, entity_id, old_value, new_value, ip, user_agent, timestamp)
- Middleware de logging automatico para acoes criticas
- Logs de: login, logout, criacao de pedido, mudanca de status, alteracoes de usuario
- Endpoint admin para consultar logs com filtros

**Testes**
- Testes de criacao automatica de logs
- Testes de consulta de logs
- Testes de permissoes (apenas admin)

**Frontend**
- Painel admin com historico de acoes
- Filtros por usuario, acao, data
- Visualizacao de detalhes de cada acao

---

## FASE 3: EXPERIENCIA DE COMPRA PREMIUM

### 3.1 Carrinho de Compras Persistente

**Backend**
- Criar modelo CarrinhoItem (usuario_id, produto_id, quantidade, customizacoes, created_at)
- CRUD de carrinho (adicionar, atualizar quantidade, remover, limpar)
- Endpoint de sincronizacao de carrinho
- Validacao de disponibilidade de produtos no carrinho
- Calculo de subtotal e total

**Testes**
- Testes de CRUD de carrinho
- Testes de sincronizacao
- Testes de validacao de produtos indisponiveis
- Testes de calculo de precos

**Frontend**
- Carrinho persistente (LocalStorage + sincronizacao com backend)
- Atualizacao de quantidade inline
- Remocao de itens
- Resumo de valores (subtotal, taxa de entrega, total)
- Botao de finalizar pedido

### 3.2 Checkout e Pagamento

**Backend**
- Criar modelo Pagamento (pedido_id, metodo, status, valor, transacao_id, created_at)
- Enum de metodos de pagamento (PIX, CARTAO_CREDITO, CARTAO_DEBITO, DINHEIRO)
- Endpoint de criar pedido a partir do carrinho
- Integracao com gateway de pagamento (Stripe ou Mercado Pago)
- Webhook para confirmacao de pagamento
- Atualizacao automatica de status do pedido

**Testes**
- Testes de criacao de pedido
- Testes de metodos de pagamento
- Testes de webhook
- Mock de gateway de pagamento

**Frontend**
- Tela de checkout dividida em etapas:
  1. Revisao do carrinho
  2. Selecao/cadastro de endereco
  3. Escolha do metodo de pagamento
  4. Confirmacao e pagamento
- Integracao com SDK do gateway de pagamento
- Loading states durante processamento
- Tela de confirmacao de pedido

### 3.3 Cupons e Promocoes

**Backend**
- Criar modelo Cupom (codigo, descricao, tipo, valor, minimo_pedido, valido_ate, ativo, uso_maximo, uso_atual)
- Tipos: PERCENTUAL, VALOR_FIXO, FRETE_GRATIS
- Endpoint de validar cupom
- Endpoint de aplicar cupom ao pedido
- Logica de calculo de desconto
- Endpoint admin para CRUD de cupons

**Testes**
- Testes de validacao de cupom
- Testes de calculo de desconto
- Testes de expiracao
- Testes de uso maximo

**Frontend**
- Campo de cupom no checkout
- Validacao em tempo real
- Exibicao do desconto aplicado
- Painel admin de gerenciamento de cupons

### 3.4 Sistema de Favoritos

**Backend**
- Criar modelo Favorito (usuario_id, produto_id, created_at)
- Endpoints: adicionar/remover favorito, listar favoritos
- Endpoint de produtos recomendados (baseado em pedidos anteriores)

**Testes**
- Testes de CRUD de favoritos
- Testes de listagem
- Testes de permissoes

**Frontend**
- Icone de coracao nos cards de produtos
- Tela de produtos favoritos
- Secao de "Seus pedidos anteriores" na home

---

## FASE 4: TRACKING E NOTIFICACOES

### 4.1 Sistema de Notificacoes em Tempo Real

**Backend**
- Implementar WebSocket para notificacoes em tempo real
- Criar modelo Notificacao (usuario_id, tipo, titulo, mensagem, lida, created_at)
- Sistema de eventos para mudancas de status de pedido
- Broadcast de notificacoes via WebSocket
- Endpoint de marcar notificacao como lida
- Endpoint de listar notificacoes

**Testes**
- Testes de conexao WebSocket
- Testes de envio de notificacoes
- Testes de marcacao como lida
- Testes de broadcast

**Frontend**
- Badge de notificacoes nao lidas no header
- Dropdown de notificacoes
- Toast notifications para atualizacoes em tempo real
- Sons sutis (opcionais) para novos eventos

### 4.2 Tracking de Pedido

**Backend**
- Criar modelo StatusHistorico (pedido_id, status, timestamp, observacao)
- Registro automatico de mudancas de status
- Endpoint de historico de status do pedido
- Estimativa de tempo de entrega
- Notificacao automatica a cada mudanca de status

**Testes**
- Testes de registro de historico
- Testes de calculo de tempo estimado
- Testes de notificacoes automaticas

**Frontend**
- Tela de detalhes do pedido com timeline visual
- Barra de progresso do status
- Tempo estimado de entrega
- Opcao de cancelamento (apenas para status PENDENTE)
- Atualizacao em tempo real via WebSocket

### 4.3 Notificacoes Multi-Canal

**Backend**
- Sistema de templates de notificacao
- Integracao com servico de SMS (Twilio)
- Integracao com WhatsApp Business API
- Push notifications (Firebase Cloud Messaging)
- Preferencias de notificacao do usuario (email, SMS, push, whatsapp)
- Fila de processamento assincrono (Celery + Redis)

**Testes**
- Testes de envio de SMS
- Testes de push notifications
- Testes de preferencias de usuario
- Mock de servicos externos

**Frontend**
- Tela de preferencias de notificacoes
- Solicitacao de permissao para push notifications
- Service Worker para PWA

---

## FASE 5: ANALYTICS E DASHBOARDS

### 5.1 Dashboard do Cliente

**Backend**
- Endpoint de estatisticas do usuario (total gasto, pedidos, produto favorito)
- Endpoint de historico de pedidos com paginacao e filtros
- Endpoint de pedido recorrente (repetir ultimo pedido)

**Testes**
- Testes de calculo de estatisticas
- Testes de paginacao
- Testes de pedido recorrente

**Frontend**
- Dashboard pessoal com cards de estatisticas
- Grafico de gastos ao longo do tempo
- Lista de pedidos anteriores
- Botao de "Pedir novamente"
- Exportacao de historico (PDF)

### 5.2 Dashboard Administrativo

**Backend**
- Endpoint de metricas gerenciais (vendas por periodo, produtos mais vendidos, ticket medio)
- Endpoint de relatorio de pedidos (filtros avancados, exportacao CSV)
- Endpoint de analise de desempenho (tempo medio de preparo, taxa de cancelamento)
- Endpoint de gestao de estoque (produtos com baixo estoque)

**Testes**
- Testes de calculo de metricas
- Testes de filtros
- Testes de exportacao
- Testes de permissoes (apenas admin)

**Frontend**
- Dashboard executivo com KPIs principais
- Graficos interativos (vendas, pedidos por status, produtos top)
- Filtros por periodo (hoje, semana, mes, personalizado)
- Tabela de pedidos em tempo real
- Exportacao de relatorios

### 5.3 Sistema de Avaliacoes

**Backend**
- Criar modelo Avaliacao (pedido_id, usuario_id, nota, comentario, created_at)
- Endpoint de criar avaliacao (apenas para pedidos entregues)
- Endpoint de listar avaliacoes de um produto
- Calculo de media de avaliacoes
- Sistema de resposta do estabelecimento

**Testes**
- Testes de criacao de avaliacao
- Testes de validacao (apenas pedidos entregues)
- Testes de calculo de media
- Testes de resposta

**Frontend**
- Modal de avaliacao apos entrega
- Exibicao de estrelas e comentarios nos produtos
- Filtros de avaliacoes (mais recentes, mais relevantes)
- Interface de resposta para admin

---

## FASE 6: PERFORMANCE E ESCALABILIDADE

### 6.1 Sistema de Cache

**Backend**
- Configuracao de Redis para cache
- Cache de listagem de produtos (TTL: 10 minutos)
- Cache de categorias (TTL: 30 minutos)
- Cache de configuracoes do sistema
- Invalidacao inteligente de cache (ao atualizar produtos)
- Cache de sessoes de usuario

**Testes**
- Testes de cache hit/miss
- Testes de invalidacao
- Testes de TTL

### 6.2 Otimizacao de Queries

**Backend**
- Implementar paginacao em todas as listagens
- Schema de resposta paginada (items, total, page, page_size, total_pages)
- Eager loading para evitar N+1 queries
- Indices compostos em queries frequentes
- Query optimization para dashboard (queries agregadas)
- Connection pooling otimizado

**Testes**
- Testes de paginacao
- Testes de performance (tempo de resposta)
- Testes de queries complexas

**Frontend**
- Componente de paginacao reutilizavel
- Infinite scroll em listagens longas
- Loading skeletons
- Lazy loading de imagens

### 6.3 Background Tasks

**Backend**
- Configuracao de Celery com Redis
- Tasks assincronas para envio de emails
- Tasks assincronas para notificacoes
- Tasks para processamento de pagamentos
- Tasks para geracao de relatorios
- Cronjobs para limpeza de dados antigos
- Monitoring de tasks (Flower)

**Testes**
- Testes de tasks assincronas
- Testes de retry de tasks falhadas
- Testes de cronjobs

**Frontend**
- Indicadores de processamento assincrono
- Notificacoes quando tasks sao concluidas

---

## FASE 7: INFRAESTRUTURA E DEVOPS

### 7.1 Containerizacao

**Backend**
- Dockerfile multi-stage otimizado
- docker-compose.yml para desenvolvimento (backend, postgres, redis, celery, flower)
- docker-compose.prod.yml para producao
- .dockerignore otimizado
- Health checks nos containers
- Volumes para persistencia de dados

**Testes**
- Testes rodam em container isolado
- Garantir que testes funcionam em ambiente Docker

**Frontend**
- Dockerfile para aplicacao React
- Nginx para servir arquivos estaticos
- Build otimizado para producao

### 7.2 Database Migration

**Backend**
- Configuracao completa do Alembic
- Migration inicial com todos os modelos
- Migrations para cada mudanca de schema
- Seed data para desenvolvimento
- Scripts de backup e restore
- Migracao de SQLite para PostgreSQL

**Testes**
- Testes de migrations (up e down)
- Testes de seed data

### 7.3 CI/CD Pipeline

**Backend**
- Configuracao de GitHub Actions
- Pipeline de testes automatizados
- Linting e formatacao automatica (black, flake8, isort)
- Verificacao de type hints (mypy)
- Analise de seguranca (bandit)
- Build e push de imagens Docker
- Deploy automatico para staging
- Deploy manual para producao

**Testes**
- Todos os testes devem passar no CI
- Coverage report no CI

**Frontend**
- Pipeline de build e testes
- Deploy automatico para Vercel/Netlify

### 7.4 Monitoring e Observabilidade

**Backend**
- Logging estruturado em JSON
- Correlation IDs em todas as requisicoes
- Middleware de request/response logging
- Mascaramento de dados sensiveis em logs
- Integracao com Sentry para error tracking
- Metricas Prometheus expostas (/metrics)
- Dashboard Grafana com alertas
- APM (Application Performance Monitoring)

**Testes**
- Testes de logging
- Testes de correlation ID
- Testes de metricas

**Frontend**
- Integracao com Sentry para erros do frontend
- Analytics (Google Analytics ou Plausible)
- Real User Monitoring

---

## FASE 8: FEATURES AVANCADAS

### 8.1 Sistema de Fidelidade

**Backend**
- Criar modelo PontosFidelidade (usuario_id, pontos, historico)
- Sistema de acumulo de pontos por valor gasto
- Sistema de resgate de pontos (descontos)
- Niveis de fidelidade (Bronze, Prata, Ouro, Diamante)
- Beneficios por nivel (frete gratis, descontos exclusivos)

**Testes**
- Testes de acumulo de pontos
- Testes de resgate
- Testes de niveis

**Frontend**
- Card de pontos no perfil
- Historico de pontos
- Catalogo de recompensas
- Badge de nivel de fidelidade

### 8.2 Sistema de Agendamento

**Backend**
- Criar modelo Agendamento (usuario_id, data_entrega, hora_entrega)
- Validacao de horarios disponiveis
- Bloqueio de horarios com capacidade atingida
- Notificacao de lembrete antes da entrega

**Testes**
- Testes de validacao de horarios
- Testes de capacidade
- Testes de notificacoes

**Frontend**
- Seletor de data e hora no checkout
- Calendario interativo
- Indicacao visual de disponibilidade

### 8.3 Multiplataforma

**Backend**
- API REST ja esta pronta
- Adicionar suporte a GraphQL (opcional)
- Otimizacoes para mobile

**Testes**
- Testes de endpoints GraphQL

**Frontend**
- PWA (Progressive Web App) completo
- App mobile React Native ou Flutter
- Suporte offline para navegacao
- Push notifications nativas

### 8.4 Internacionalizacao

**Backend**
- Sistema de mensagens traduziveis
- Endpoint de configuracao de idioma
- Suporte a multiplas moedas
- Formatacao de datas/valores por locale

**Testes**
- Testes de traducao
- Testes de formatacao

**Frontend**
- Seletor de idioma
- Traducao de textos estaticos
- Formatacao de valores monetarios

---

## FASE 9: INTEGRACOES EXTERNAS

### 9.1 Integracao com Delivery Apps

**Backend**
- Webhooks para receber pedidos de iFood, Rappi, Uber Eats
- Padronizacao de formato de pedidos
- Sincronizacao de cardapio
- Atualizacao de status de pedidos

**Testes**
- Testes de webhooks
- Testes de sincronizacao
- Mock de APIs externas

**Frontend**
- Indicador visual de origem do pedido
- Painel de gerenciamento de integracoes

### 9.2 Sistema de Marketing

**Backend**
- Integracao com Mailchimp ou SendGrid
- Segmentacao de clientes
- Campanhas de email marketing
- Analise de campanhas

**Testes**
- Testes de segmentacao
- Mock de servicos

**Frontend**
- Tela de assinatura de newsletter
- Preferencias de marketing

### 9.3 Chat de Suporte

**Backend**
- Sistema de chat em tempo real (WebSocket)
- Atribuicao automatica de atendentes
- Historico de conversas
- Chatbot para FAQs

**Testes**
- Testes de chat
- Testes de atribuicao

**Frontend**
- Widget de chat
- Interface de admin para atendimento

---

## FASE 10: REFINAMENTO FINAL

### 10.1 Acessibilidade

**Backend**
- Garantir que endpoints retornam dados semanticos

**Frontend**
- WCAG 2.1 AA compliance
- Navegacao por teclado completa
- Screen reader friendly
- Alto contraste
- Tamanhos de fonte ajustaveis

### 10.2 Performance Frontend

**Frontend**
- Code splitting
- Tree shaking
- Compressao de assets
- CDN para imagens
- Otimizacao de bundle
- Lighthouse score 90+
- Tempo de carregamento < 3s

### 10.3 Testes E2E

**Backend e Frontend**
- Testes end-to-end com Playwright
- Testes de jornadas criticas
- Testes de regressao visual
- Testes de performance

### 10.4 Documentacao Final

**Backend**
- API documentation completa
- Postman/Insomnia collection
- OpenAPI 3.0 spec
- Diagramas de arquitetura
- Guia de deployment

**Frontend**
- Storybook de componentes
- Guia de estilo
- Documentacao de design system

---

## PRINCIPIOS DE IMPLEMENTACAO

### Ordem de Execucao

Para cada funcionalidade:
1. Backend: Implementar models, schemas, endpoints
2. Backend: Escrever testes unitarios e de integracao
3. Backend: Validar cobertura de testes
4. Frontend: Implementar interfaces e componentes
5. Frontend: Integrar com API
6. Frontend: Testes de componentes e integracao
7. Validacao E2E da funcionalidade completa
8. Deploy incremental

### Qualidade

- Manter cobertura de testes sempre acima de 80%
- Code review obrigatorio
- Linting e formatacao automaticos
- Documentacao inline (docstrings, comentarios)
- Commits semanticos
- Versionamento semantico

### Performance

- Response time < 200ms para 95% das requisicoes
- Lighthouse score > 90
- Otimizacao de queries
- Cache estrategico
- Lazy loading

### Seguranca

- OWASP Top 10 compliance
- Sanitizacao de inputs
- Rate limiting
- Auditoria de acoes criticas
- Criptografia de dados sensiveis
- HTTPS em producao

---

## NOTAS FINAIS

A migracao para PostgreSQL pode ser feita a qualquer momento, preferencialmente antes da Fase 3, quando o volume de dados e complexidade das queries aumenta.

O sistema final sera comparavel em robustez e features as principais plataformas de delivery do mercado, com codigo limpo, testado e preparado para escalar.
