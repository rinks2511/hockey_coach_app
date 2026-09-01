# Developer Onboarding & Multi-Team Scaling Guide

Welcome to the **HV Myra Matchday Board Application** codebase! This guide provides everything a new developer or incoming engineering team needs to understand, run, test, extend, and deploy the application.

---

## 1. Quick Start Local Development

### 1.1 Prerequisites
* Python 3.11+
* Git
* (Optional) Google Cloud SDK (`gcloud`) for deployment

### 1.2 Local Setup Instructions

```bash
# 1. Clone repository
git clone https://github.com/your-org/hockey_coach_app.git
cd hockey_coach_app

# 2. Create virtual environment & activate
python3 -m venv .venv
source .venv/bin/activate

# 3. Install backend dependencies
pip install -r backend/requirements.txt

# 4. Start Uvicorn development server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8085 --reload
```

Open your browser at `http://127.0.0.1:8085` to interact with the application.

---

## 2. Running Automated Tests

All backend routers (`auth`, `config`, `tactics`, `teams`) must have 100% test pass rates before pushing code.

```bash
# Run pytest test suite from project root
PYTHONPATH=. pytest backend/tests/ -v
```

---

## 3. How Multi-Tenancy & Multi-Team Support Works

The application supports multiple team formats (e.g. `MO10` 8v8, `Trimmers` 11v11) out of the box.

### Data Partitioning Architecture
* Every setting, saved tactics snapshot, and player availability record is isolated by `team_id`.
* Backend routes enforce `WHERE team_id = ?` checks.

### Onboarding a New Team Tomorrow
To add a new team (e.g. `JO12` or `Seniors1`), send a `POST` request to `/api/teams`:

```bash
curl -X POST "http://127.0.0.1:8085/api/teams" \
     -H "Content-Type: application/json" \
     -d '{
           "team_id": "JO12",
           "coach_emails": ["coach.jo12@hvmyra.nl"],
           "squad_players": ["Liam", "Noah", "Lucas", "Ethan", "Mason"]
         }'
```

The system will automatically initialize isolated settings for `JO12`, and it will immediately appear in the top header team dropdown in the UI.

---

## 4. Deployment Workflow

Deployments are executed to **Google Cloud Run** (`europe-west4`).

```bash
# 1. Verify tests locally
PYTHONPATH=. pytest backend/tests/

# 2. Trigger Cloud Run container build & deployment
./deployment/deploy_cloudrun.sh
```

---

## 5. Architectural Decision Records (ADRs)

Before making structural changes, review the decision records in [`docs/adr/`](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/adr/README.md):
* [ADR 0001: FastAPI & Cloud Run](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/adr/0001-use-fastapi-and-cloudrun.md)
* [ADR 0002: Multi-Tenant Team Partitioning](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/adr/0002-multi-tenant-team-partitioning.md)
* [ADR 0003: Ephemeral SQLite to Cloud SQL Migration](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/adr/0003-database-migration-sqlite-to-cloudsql.md)
