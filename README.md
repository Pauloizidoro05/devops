# TaskFlow API

Projeto da disciplina **Integração DevOps** — Ciência da Computação 2026/2 (Prof. Danilo Silva).

API simples de gerenciamento de tarefas (to-do list), construída em **Python + FastAPI**,
usada como base para evoluir através das três fases da disciplina (CI → IaC/CD → DevSecOps/Observabilidade).

## Stack

- **Linguagem:** Python 3.11+
- **Framework:** FastAPI
- **ORM / Banco de dados:** SQLAlchemy + SQLite (fase 1) → PostgreSQL via Docker Compose (fase 2)
- **Testes:** Pytest + FastAPI TestClient
- **CI:** GitHub Actions

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A aplicação sobe em `http://127.0.0.1:8000`.
A interface de interação (Swagger UI, gerada automaticamente pelo FastAPI) fica em:

```
http://127.0.0.1:8000/docs
```

## Como rodar os testes

```bash
pytest tests/ -v
```

## Endpoints principais

| Método | Rota           | Descrição                  |
|--------|----------------|-----------------------------|
| GET    | /health        | Health check (usado no CI)  |
| POST   | /tasks         | Cria uma tarefa             |
| GET    | /tasks         | Lista tarefas               |
| GET    | /tasks/{id}    | Busca uma tarefa por id     |
| PATCH  | /tasks/{id}    | Atualiza uma tarefa         |
| DELETE | /tasks/{id}    | Remove uma tarefa           |

## Estratégia de branching (Trunk-Based Development)

- `main`: branch principal, sempre estável e protegida (build/CI verde obrigatório para merge).
- Desenvolvimento em branches de curta duração a partir da `main`, no padrão:
  - `feature/<nome-curto>` — novas funcionalidades
  - `fix/<nome-curto>` — correções de bugs
  - `chore/<nome-curto>` — tarefas de manutenção (deps, configs, docs)
- Pull Requests obrigatórios para integrar na `main`; nenhum push direto é permitido.
- Regras de proteção configuradas na `main` (GitHub → Settings → Branches):
  - Exigir Pull Request antes de merge.
  - Exigir que os checks de CI passem antes de habilitar o merge.
  - Exigir pelo menos 1 aprovação de revisão (quando o grupo tiver mais de 1 integrante ativo).
  - Proibir force-push e deleção da branch.

## Padrão de commits

Utilizamos o padrão **Conventional Commits**:

```
<tipo>(<escopo opcional>): <descrição curta>

Exemplos:
feat(tasks): adiciona endpoint de atualização parcial de tarefa
fix(api): corrige status code de tarefa não encontrada
test(tasks): adiciona testes de integração do CRUD
chore(ci): configura pipeline do GitHub Actions
docs(readme): documenta estratégia de branching
```

Tipos usados: `feat`, `fix`, `test`, `chore`, `docs`, `refactor`.

## Divisão de papéis do grupo

| Papel                        | Responsabilidades principais                                   |
|-------------------------------|------------------------------------------------------------------|
| Desenvolvedor(a)               | Implementação das funcionalidades (endpoints, regras de negócio) |
| Qualidade                      | Escrita e manutenção dos testes automatizados, revisão de PRs    |
| Operações / Infraestrutura     | Pipeline de CI/CD, containerização, observabilidade (fases 2 e 3)|

## Pipeline de CI (GitHub Actions)

Definido em `.github/workflows/ci.yml`. É executado automaticamente a cada `push` ou
`pull_request` direcionado à branch `main`, e realiza:

1. Checkout do código.
2. Setup do Python (matriz de versões 3.11 e 3.12).
3. Instalação das dependências (`requirements.txt`).
4. Execução da suíte de testes automatizados (`pytest`).
5. Publicação do relatório de testes como artefato do workflow.

## Roadmap das próximas fases

- **Fase 2 (A2):** Dockerfile, docker-compose com PostgreSQL, pipeline de CD publicando
  imagem em um Container Registry, gestão de segredos via CI/CD e versionamento semântico.
- **Fase 3 (A3):** SAST (SonarQube/Trivy), observabilidade com métricas/logs e dashboard
  no Grafana, documentação técnica final e live demo do pipeline completo.
