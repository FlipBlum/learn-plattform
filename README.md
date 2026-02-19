# Learn Plattform

Mono-Repo fuer die Lernplattform learn.innovique.ai.

## Projektstruktur

```
/frontend   - Vue 3 / Nuxt 3 App
/api        - Python FastAPI Backend
/worker     - Python Cronjob/Scheduler (APScheduler)
/infra      - Docker, docker-compose, Nginx
/.github    - CI/CD, PR-Template, CODEOWNERS
```

## Voraussetzungen

- Node.js 22+
- Python 3.12+
- Docker & Docker Compose

## Setup

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Die App laeuft auf http://localhost:3000.

### API

```bash
cd api
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# .env Werte eintragen
uvicorn app.main:app --reload
```

Die API laeuft auf http://localhost:8000.

### Worker

```bash
cd worker
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python main.py
```

### Docker (alle Services)

```bash
cd infra
cp .env.example .env
# .env Werte eintragen
docker compose up --build
```

## Entwicklung

### Linting & Formatting

```bash
# Frontend
cd frontend
npm run lint
npm run format

# API
cd api
ruff check .
black .
```

### Tests

```bash
# Frontend
cd frontend
npm run test

# API
cd api
pytest

# Worker
cd worker
pytest
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

## CI/CD

GitHub Actions laufen bei Push auf `main` und bei Pull Requests:
- `lint-frontend` - ESLint + Prettier Check
- `test-frontend` - Vitest
- `lint-api` - Ruff + Black Check
- `test-api` - pytest
