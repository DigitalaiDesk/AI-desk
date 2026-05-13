# AI-desk — AI Discoverability Operating System

Monorepo for a desktop-first platform that unifies SEO, AEO, GEO, AI visibility analytics, retrieval optimization, and entity intelligence.

## Monorepo Layout

- `apps/desktop`: Tauri + React desktop shell
- `apps/web`: React web app scaffold
- `apps/api`: FastAPI backend
- `packages/*`: shared UI, engines, types, and config
- `services/*`: infrastructure adapters (Qdrant, Neo4j, local model runtime)
- `infra/*`: Docker and database migrations

## Quick start

```bash
pnpm install
pnpm dev
```

Backend:

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```
