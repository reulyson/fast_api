# Fast API

API REST desenvolvida com FastAPI.

## Descrição

Este projeto é uma API moderna e de alta performance construída com **FastAPI**, seguindo as melhores práticas de desenvolvimento Python (PEP-8, PEP-257, PEP-484). Oferece um CRUD completo de usuários com persistência em banco de dados SQLite e documentação OpenAPI automática. Inclui camada de persistência com **SQLAlchemy** e **Alembic** para migrações de banco de dados.

### Funcionalidades

- ✅ CRUD completo de usuários (Create, Read, Update, Delete)
- ✅ Validação de dados com Pydantic
- ✅ Validação de unicidade (username e email únicos)
- ✅ Paginação na listagem de usuários
- ✅ Tratamento de erros com códigos HTTP apropriados
- ✅ Documentação interativa (Swagger UI e ReDoc)
- ✅ Testes automatizados com pytest
- ✅ Migrações de banco de dados com Alembic

## Tecnologias

- **FastAPI** — Framework web assíncrono
- **SQLAlchemy** — ORM para banco de dados
- **Pydantic** — Validação e serialização
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

Crie um arquivo `.env` na raiz do projeto com a URL do banco de dados:

```bash
DATABASE_URL=sqlite:///./database.db
```

### 6. Executar migrações (opcional)

Para criar/atualizar as tabelas no banco de dados:

```bash
alembic upgrade head
```

## Rotas da API

| Método   | Rota           | Descrição                    | Status Codes        |
|----------|----------------|------------------------------|---------------------|
| GET      | `/`            | Mensagem de boas-vindas      | 200                 |
| POST     | `/users/`      | Cria um usuário               | 201, 409            |
| GET      | `/users/`      | Lista todos os usuários       | 200                 |
| GET      | `/users/{id}`  | Retorna um usuário pelo id    | 200, 404            |
| PUT      | `/users/{id}`  | Atualiza um usuário pelo id   | 200, 404, 409       |
| DELETE   | `/users/{id}`  | Remove um usuário pelo id     | 200, 404            |

### Detalhamento das Rotas

- **GET /** — Retorna `{"message": "Hello, World!"}`.

- **POST /users/** — Cria um novo usuário.
  - **Body**: `{"username": "string", "email": "string", "password": "string"}`
  - **Sucesso (201)**: Retorna o usuário criado (sem senha): `{"id": int, "username": "string", "email": "string"}`
  - **Erro (409)**: Quando username ou email já existem: `{"detail": "username já existe!"}` ou `{"detail": "email já existe!"}`

- **GET /users/** — Lista todos os usuários com paginação.
  - **Query params**: `limit` (padrão: 10), `offset` (padrão: 0)
  - **Resposta**: `{"users": [{"id": int, "username": "string", "email": "string"}, ...]}`

- **GET /users/{user_id}** — Retorna um usuário específico.
  - **Sucesso (200)**: `{"id": int, "username": "string", "email": "string"}`
  - **Erro (404)**: `{"detail": "Not Found"}`

- **PUT /users/{user_id}** — Atualiza um usuário existente.
  - **Body**: `{"username": "string", "email": "string", "password": "string"}`
  - **Sucesso (200)**: Retorna o usuário atualizado: `{"id": int, "username": "string", "email": "string"}`
  - **Erro (404)**: Usuário não encontrado: `{"detail": "Not Found"}`
  - **Erro (409)**: Username ou email já existem em outro usuário: `{"detail": "username ou email já existem!"}`

- **DELETE /users/{user_id}** — Remove um usuário.
  - **Sucesso (200)**: `{"message": "User delete"}`
  - **Erro (404)**: `{"detail": "Not Found"}`

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
│   ├── models.py       # Modelos ORM (User) com SQLAlchemy
│   ├── schemas.py      # Modelos Pydantic (Message, UserSchema, UserPublic, UserList, ErrorDetail)
│   ├── database.py     # Configuração da sessão do banco de dados
│   └── settings.py     # Configurações (DATABASE_URL) via pydantic-settings
├── migrations/         # Migrações Alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/
│   ├── conftest.py     # Fixtures (cliente, sessão, mock_db_time)
│   ├── test_app.py     # Testes da API
│   └── test_db.py      # Testes do banco de dados
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

- **Schemas de entrada**: `user: UserSchema` (dados recebidos da requisição)
- **Objetos do banco**: `user_db` (objetos User carregados do banco)
- **Variáveis temporárias**: `existing_user` (para verificações de duplicatas)

## Licença

Este projeto está sob a licença MIT.
