# AI Desk — Monorepo Foundation

AI Desk is an agency intelligence platform for SEO/AEO/GEO operations. This repository is organized as a monorepo with separate app surfaces, shared platform docs, and implementation templates.

## Repository architecture

- `apps/backend` — FastAPI backend scaffold with crawl, embeddings, entity, scoring, and visibility service modules plus tests.
- `apps/frontend` — desktop/dashboard UI scaffold (currently includes the intelligence dashboard page structure).
- `docs` — architecture and operating-system specifications.
- `templates/workflows` — reusable workflow templates for audits and content refresh operations.
- `integrations` — integration contracts for external CMS systems.

## Current platform modules in the foundation branch

- Crawl orchestration models, schemas, and API route scaffolding.
- Embedding/indexing, entity extraction, scoring, and simulation service abstractions.
- Initial SQL migration for intelligence backend storage.
- Agency OS specification for client/project/task/reporting lifecycle.

## Quick start (backend)

```bash
cd apps/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Quality checks

From repository root:

```bash
pytest apps/backend/tests
python -m compileall apps/backend/app
```

## Implementation roadmap

Planned delivery proceeds in small, reviewable phases:

1. Resolve merge blockers and align docs with architecture.
2. Complete crawler engine and crawl result APIs.
3. Add semantic chunking + embeddings + vector persistence.
4. Add entity extraction normalization + graph persistence.
5. Implement SEO/AEO/GEO scoring engines with recommendations.
6. Implement AI visibility simulation and explanation outputs.
7. Implement agency OS workflows (workspaces/projects/tasks/approvals).
8. Deliver dashboards and exportable reports.
