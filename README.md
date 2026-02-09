# Fast API

API REST desenvolvida com FastAPI.

## Descrição

Este projeto é uma API moderna e de alta performance construída com **FastAPI**, seguindo as melhores práticas de desenvolvimento Python (PEP-8, PEP-257, PEP-484). Oferece CRUD completo de **usuários** e **produtos** com persistência em banco de dados SQLite e documentação OpenAPI automática. Inclui camada de persistência com **SQLAlchemy** e **Alembic** para migrações de banco de dados.

### Funcionalidades

- ✅ CRUD completo de usuários (Create, Read, Update, Delete)
- ✅ CRUD completo de produtos (Create, Read, Update, Delete)
- ✅ Autenticação JWT (OAuth2) para rotas protegidas
- ✅ Validação de dados com Pydantic
- ✅ Validação de unicidade (username, email e nome de produto únicos)
- ✅ Paginação na listagem de usuários e produtos
- ✅ Tratamento de erros com códigos HTTP apropriados
- ✅ Documentação interativa (Swagger UI e ReDoc)
- ✅ Testes automatizados com pytest
- ✅ Migrações de banco de dados com Alembic

## Tecnologias

- **FastAPI** — Framework web assíncrono
- **SQLAlchemy** — ORM para banco de dados
- **Pydantic** — Validação e serialização
- **PyJWT** — Tokens JWT para autenticação
- **pwdlib** — Hash e verificação de senhas
- **Alembic** — Migrações de banco
- **pydantic-settings** — Configurações via variáveis de ambiente

## Pré-requisitos

- **Python**: 3.13+
- **pipx**: Para instalar ferramentas Python isoladas
- **Poetry**: Para gerenciamento de dependências

## Instalação

### 1. Instalar o pipx

```bash
pip install --user pipx
pipx ensurepath
```

### 2. Instalar o Poetry

```bash
pipx install poetry
pipx inject poetry poetry-plugin-shell
```

### 3. Clonar e configurar o projeto

```bash
git clone <url-do-repositorio>
cd fast_api
```

### 4. Configurar o ambiente

```bash
poetry env use 3.13
poetry install
```

### 5. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
DATABASE_URL=sqlite:///./database.db
SECRET_KEY=sua_chave_secreta_com_pelo_menos_32_caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Executar migrações (opcional)

Para criar/atualizar as tabelas no banco de dados:

```bash
alembic upgrade head
```

## Rotas da API

| Método   | Rota              | Descrição                     | Autenticação | Status Codes        |
|----------|-------------------|-------------------------------|--------------|---------------------|
| GET      | `/`               | Mensagem de boas-vindas       | Não          | 200                 |
| POST     | `/auth/`          | Obtém token de acesso         | Não          | 200, 401            |
| POST     | `/users/`         | Cria um usuário               | Sim          | 201, 409            |
| GET      | `/users/`         | Lista todos os usuários       | Sim          | 200, 401            |
| GET      | `/users/{id}`     | Retorna um usuário pelo id    | Sim          | 200, 401, 404       |
| PUT      | `/users/{id}`     | Atualiza um usuário pelo id   | Sim          | 200, 401, 403, 409  |
| DELETE   | `/users/{id}`     | Remove um usuário pelo id     | Sim          | 200, 401, 403       |
| POST     | `/products/`      | Cria um produto               | Sim          | 201, 409            |
| GET      | `/products/`      | Lista todos os produtos       | Sim          | 200, 401            |
| GET      | `/products/{id}`  | Retorna um produto pelo id    | Sim          | 200, 401, 404       |
| PUT      | `/products/{id}`  | Atualiza um produto pelo id   | Sim          | 200, 401, 404, 409  |
| DELETE   | `/products/{id}`  | Remove um produto pelo id     | Sim          | 200, 401, 404       |

### Autenticação

As rotas protegidas exigem o header `Authorization: Bearer <token>`. Para obter o token:

```bash
curl -X POST "http://127.0.0.1:8000/auth/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=email@exemplo.com&password=suasenha"
```

Resposta: `{"access_token": "...", "token_type": "Bearer"}`

### Detalhamento das Rotas

- **GET /** — Retorna `{"message": "Hello, World!"}`. Pública.

- **POST /auth/** — Obtém token JWT para autenticação.
  - **Body** (form-urlencoded): `username` (email), `password`
  - **Sucesso (200)**: `{"access_token": "string", "token_type": "Bearer"}`
  - **Erro (401)**: `{"detail": "Email ou senha incorretos"}` ou `{"detail": "Senha incorreta"}`

- **POST /users/** — Cria um novo usuário. Requer autenticação.
  - **Headers**: `Authorization: Bearer <token>`
  - **Body**: `{"username": "string", "email": "string", "password": "string"}`
  - **Sucesso (201)**: Retorna o usuário criado: `{"id": int, "username": "string", "email": "string"}`
  - **Erro (401)**: Token inválido ou ausente: `{"detail": "Could not validate credentials"}`
  - **Erro (409)**: Username ou email já existem: `{"detail": "username já existe!"}` ou `{"detail": "email já existe!"}`

- **GET /users/** — Lista todos os usuários com paginação. Requer autenticação.
  - **Headers**: `Authorization: Bearer <token>`
  - **Query params**: `limit` (padrão: 10), `offset` (padrão: 0)
  - **Resposta**: `{"users": [{"id": int, "username": "string", "email": "string"}, ...]}`
  - **Erro (401)**: Token inválido ou ausente

- **GET /users/{user_id}** — Retorna um usuário específico. Requer autenticação.
  - **Headers**: `Authorization: Bearer <token>`
  - **Sucesso (200)**: `{"id": int, "username": "string", "email": "string"}`
  - **Erro (401)**: Token inválido ou ausente
  - **Erro (404)**: `{"detail": "Not Found"}`

- **PUT /users/{user_id}** — Atualiza um usuário existente. Requer autenticação. Só o próprio usuário pode atualizar seus dados.
  - **Headers**: `Authorization: Bearer <token>`
  - **Body**: `{"username": "string", "email": "string", "password": "string"}`
  - **Sucesso (200)**: Retorna o usuário atualizado: `{"id": int, "username": "string", "email": "string"}`
  - **Erro (401)**: Token inválido ou ausente
  - **Erro (403)**: Tentativa de atualizar outro usuário: `{"detail": "Você não tem permissão para atualizar este usuário"}`
  - **Erro (409)**: Username ou email já existem em outro usuário: `{"detail": "username ou email já existem!"}`

- **DELETE /users/{user_id}** — Remove um usuário. Requer autenticação. Só o próprio usuário pode se remover.
  - **Headers**: `Authorization: Bearer <token>`
  - **Sucesso (200)**: `{"message": "User delete"}`
  - **Erro (401)**: Token inválido ou ausente
  - **Erro (403)**: Tentativa de remover outro usuário: `{"detail": "Você não tem permissão para remover este usuário"}`

### Rotas de Produtos

- **POST /products/** — Cria um novo produto. Requer autenticação.
  - **Headers**: `Authorization: Bearer <token>`
  - **Body**: `{"name": "string", "description": "string", "price": float}`
  - **Sucesso (201)**: Retorna o produto criado: `{"id": int, "name": "string", "description": "string", "price": float}`
  - **Erro (401)**: Token inválido ou ausente
  - **Erro (409)**: Nome já existe: `{"detail": "Produto já existe!"}`

- **GET /products/** — Lista todos os produtos com paginação. Requer autenticação.
  - **Headers**: `Authorization: Bearer <token>`
  - **Query params**: `limit` (padrão: 10), `offset` (padrão: 0)
  - **Resposta**: `{"products": [{"id": int, "name": "string", "description": "string", "price": float}, ...]}`
  - **Erro (401)**: Token inválido ou ausente

- **GET /products/{product_id}** — Retorna um produto pelo id. Requer autenticação.
  - **Headers**: `Authorization: Bearer <token>`
  - **Sucesso (200)**: `{"id": int, "name": "string", "description": "string", "price": float}`
  - **Erro (401)**: Token inválido ou ausente
  - **Erro (404)**: `{"detail": "Produto não encontrado!"}`

- **PUT /products/{product_id}** — Atualiza um produto. Requer autenticação.
  - **Headers**: `Authorization: Bearer <token>`
  - **Body**: `{"name": "string", "description": "string", "price": float}`
  - **Sucesso (200)**: Retorna o produto atualizado
  - **Erro (401)**: Token inválido ou ausente
  - **Erro (404)**: `{"detail": "Produto não encontrado!"}`
  - **Erro (409)**: Nome já existe: `{"detail": "Nome de produto já existe!"}`

- **DELETE /products/{product_id}** — Remove um produto. Requer autenticação.
  - **Headers**: `Authorization: Bearer <token>`
  - **Sucesso (200)**: `{"message": "Produto deletado!"}`
  - **Erro (401)**: Token inválido ou ausente
  - **Erro (404)**: `{"detail": "Produto não encontrado!"}`

## Como Usar

### Ativar o ambiente virtual

```bash
poetry shell
```

### Iniciar o servidor de desenvolvimento

```bash
task run
```

Ou diretamente:

```bash
fastapi dev fast_api/app.py
```

A API estará disponível em: **http://127.0.0.1:8000**

### Documentação interativa

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Comandos Disponíveis (Taskipy)

| Comando       | Descrição                          |
|---------------|------------------------------------|
| `task run`    | Inicia o servidor de desenvolvimento |
| `task lint`   | Verifica o código com Ruff         |
| `task format` | Formata o código com Ruff          |
| `task test`   | Executa os testes com cobertura    |

## Estrutura do Projeto

```
fast_api/
├── fast_api/
│   ├── __init__.py
│   ├── app.py          # Aplicação principal e rotas da API
│   ├── models.py       # Modelos ORM (User, Product) com SQLAlchemy
│   ├── database.py     # Configuração da sessão do banco de dados
│   ├── security.py     # Autenticação JWT, hash de senhas, get_current_user
│   ├── settings.py     # Configurações (DATABASE_URL, SECRET_KEY) via pydantic-settings
│   ├── schemas/        # Modelos Pydantic
│   │   ├── schemas.py      # Message, ErrorDetail, Token, FilterParams
│   │   ├── user_schema.py  # UserSchema, UserPublic, UserList
│   │   └── product_schema.py # ProductSchema, ProductPublic, ProductList
│   └── routers/
│       ├── auth.py     # Rota de autenticação (POST /auth/)
│       ├── users.py    # Rotas CRUD de usuários
│       └── product.py  # Rotas CRUD de produtos
├── migrations/         # Migrações Alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/
│   ├── conftest.py     # Fixtures (client, session, mock_user, mock_product, token)
│   ├── test_app.py     # Testes da API principal
│   ├── test_db.py      # Testes do banco de dados
│   ├── test_security.py # Testes de autenticação JWT
│   └── routers/
│       ├── test_auth.py     # Testes da rota de autenticação
│       ├── test_user.py     # Testes das rotas de usuários
│       └── test_product.py  # Testes das rotas de produtos
├── alembic.ini        # Configuração do Alembic
├── pyproject.toml     # Configurações do projeto
├── poetry.lock        # Lock das dependências
└── README.md
```

## Ferramentas de Desenvolvimento

- **Ruff**: Linter e formatador de código (PEP-8, linha ≤ 79 caracteres, aspas simples)
- **pytest**: Framework de testes
- **pytest-cov**: Cobertura de testes
- **taskipy**: Automação de tarefas (lint, format, test, run)
- **Alembic**: Migrações de banco de dados

## Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'feat: adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Padrões de Código

- Siga a **PEP-8** para estilo de código
- Use **aspas simples** para strings
- Mantenha linhas com no máximo **79 caracteres**
- Adicione **docstrings** (PEP-257) em módulos, classes e funções
- Use **type hints** (PEP-484) em todas as funções
- Padronize variáveis do banco de dados como `user_db` ou `db_user`

### Convenções de Nomenclatura

- **Schemas de entrada**: `user: UserSchema`, `product: ProductSchema` (dados da requisição)
- **Objetos do banco**: `user_db`, `product_db` (objetos carregados do banco)
- **Variáveis temporárias**: `existing_user`, `existing_product` (verificações de duplicatas)

## Licença

Este projeto está sob a licença MIT.
