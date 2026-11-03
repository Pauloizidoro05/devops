# Evidência de Versionamento e Rollback

Projeto TaskFlow API — Integração DevOps (A2).

## Versionamento semântico

As imagens são publicadas no GitHub Container Registry (GHCR) a cada tag `vX.Y.Z`, com as tags de imagem `X.Y.Z`, `X.Y` e `latest`:

- `ghcr.io/pauloizidoro05/taskflow-api:1.0.0`
- `ghcr.io/pauloizidoro05/taskflow-api:1.1.0`

## Fluxo executado

| Etapa | Ação | Resultado |
|---|---|---|
| 1 | Release `v1.0.0` (CD #1) | `build-push` e `deploy` com sucesso |
| 2 | Alteração proposital da porta da aplicação para 9000 e release `v1.1.0` (CD #2) | `build-push` com sucesso, `deploy` **falhou** |
| 3 | Rollback: execução manual do workflow CD com `version = 1.0.0` | `deploy` com sucesso |

## Cenário de falha (v1.1.0)

A versão 1.1.0 foi gerada com a porta da aplicação alterada de 8000 para 9000 no `Dockerfile`, mantendo o healthcheck e o smoke test em 8000.

O pipeline subiu a imagem pelo Docker Compose e testou o endpoint `/health` por até 20 tentativas. Como a aplicação não respondeu na porta esperada, o job `deploy` terminou com a mensagem `Deploy FALHOU (versão 1.1.0)` e status de falha. A versão defeituosa não foi considerada saudável.

## Procedimento de rollback

1. Em **Actions → CD → Run workflow**, informar `version = 1.0.0`.
2. O workflow (gatilho `workflow_dispatch`) pula a etapa de build e faz o deploy da imagem `1.0.0`, que já está publicada no GHCR.
3. O smoke test em `/health` passou e o job exibiu `Deploy OK (versão 1.0.0)`.

Tempo de recuperação: cerca de 1 minuto entre iniciar o rollback e ter a versão estável de volta.

## Gestão de segredos

As credenciais do banco (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) ficam em **Settings → Secrets and variables → Actions**. O pipeline as injeta como variáveis de ambiente no deploy, e nenhuma senha está no código-fonte (o repositório contém apenas o `.env.example`).

## Lições aprendidas

- O smoke test no pipeline impediu que uma versão quebrada fosse considerada válida.
- Imagens versionadas permitem voltar a uma versão estável sem rebuild.
- O rollback reutiliza o mesmo pipeline, o que o torna rápido e previsível.
- Próximo passo (fase 3): adicionar varredura de segurança (SAST e Trivy) antes da publicação da imagem.
