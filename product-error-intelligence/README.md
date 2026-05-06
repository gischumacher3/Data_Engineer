# Product Error Intelligence Pipeline

Sistema para coletar, tratar, classificar e analisar solicitações de usuários relacionadas a erros e gaps de produto, gerando KPIs, dashboards e recomendações via IA.

## Arquitetura

```text
CSV Upload
  -> Ingestion Layer
  -> Data Validation
  -> Cleaning & Standardization
  -> Classification / Enrichment
  -> Postgres / NeonDB
  -> KPIs + Dashboards
  -> Agno AI Agent
  -> Insights para Produto
```

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn src.main:app --reload
```

Por padrão, o backend usa SQLite local para facilitar o MVP. Para NeonDB, configure `DATABASE_URL` no `.env`:

```env
DATABASE_URL=postgresql+psycopg://user:password@host/dbname?sslmode=require
```

Endpoints principais:

- `POST /upload`
- `GET /requests`
- `GET /requests/summary`
- `GET /kpis`
- `GET /charts/categories`
- `GET /charts/severity`
- `POST /agent/analyze`
- `GET /pipeline-runs`
- `GET /pipeline-runs/{id}`

## Frontend

```bash
cd frontend
npm install
npm run dev
```

A aplicação abre em `http://localhost:5173` e consome a API em `http://localhost:8000`.

## Schema esperado do CSV

- `Nome do cliente`
- `Email`
- `CPF/CNPJ`
- `Telefone`
- `Empresa`
- `Problema (Descrição)`
- `Data da Solicitação`
- `Solicitação Finalizada?`

## Classificação MVP

A classificação é híbrida por desenho, mas o MVP implementa a camada controlada por regras:

- palavras-chave por categoria;
- score de confiança interno;
- severidade derivada da categoria;
- business impact score por volume, severidade, perfil de cliente e recorrência.

Quando `OPENAI_API_KEY` está configurado, o endpoint `/agent/analyze` tenta usar Agno com OpenAI. Sem chave ou em caso de falha, ele retorna uma análise determinística baseada nos KPIs.
