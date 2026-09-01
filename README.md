# 🏑 HV Myra Matchday Board Application

[![Python Backend CI](https://github.com/rinks2511/hockey_coach_app/actions/workflows/deploy.yml/badge.svg)](https://github.com/rinks2511/hockey_coach_app/actions/workflows/deploy.yml)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Cloud_Run-blue?logo=googlecloud)](https://hockey-coach-app-1083993716124.europe-west4.run.app)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A web-based tactical planning, matchday board, and squad rotation management system built for field hockey coaches, team managers, and parents. Supports multiple team configurations (e.g. Youth MO10 8v8, Senior Trimmers 11v11), dynamic pitch boards, player rotation calculation, and KNHB match rule guides.

---

## 🚀 Live Demo

* **Production URL**: [https://hockey-coach-app-1083993716124.europe-west4.run.app](https://hockey-coach-app-1083993716124.europe-west4.run.app)
* **API Documentation**: [https://hockey-coach-app-1083993716124.europe-west4.run.app/docs](https://hockey-coach-app-1083993716124.europe-west4.run.app/docs)

---

## ✨ Features

- 👑 **Coach Mode & 👪 Parent Mode (RBAC)**: Role-based access control ensuring coaches can edit tactics and lineups while parents view real-time read-only match sheets.
- 📐 **Dynamic Pitch Tactical Board**: Interactive drag-and-drop player token positioning with preset formation support (`1-2-3-2`, `1-3-3-1`, `4-3-3`, `3-4-3`).
- ✍️ **Pitch Drawing Canvas**: Freehand vector drawing, arrow placement, and zone markings for tactical explanations on tablet & mobile devices.
- ⚡ **Automated Substitution Matrix**: Equal playing time calculator and substitution schedule generator.
- 🌐 **Multi-Tenant Architecture**: Dynamic team switching (`MO10`, `Trimmers`) with isolated squad rosters and settings.

---

## 🛠️ Tech Stack & Architecture

- **Backend**: Python 3.11, FastAPI, Pydantic Settings, SQLite / Cloud SQL (PostgreSQL).
- **Frontend**: HTML5, Vanilla JavaScript (ES Modules), Custom SVG Pitch Board.
- **Deployment**: Google Cloud Run (`europe-west4`), Docker.

---

## ⚡ Quickstart Development

```bash
# 1. Clone repository
git clone git@github.com:rinks2511/hockey_coach_app.git
cd hockey_coach_app

# 2. Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# 3. Start Uvicorn development server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8085 --reload
```

Run test suite:
```bash
PYTHONPATH=. pytest backend/tests/ -v
```

---

## 📚 Documentation & Governance

- **[System Architecture](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/ARCHITECTURE.md)**
- **[Developer Onboarding & Multi-Team Guide](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/DEVELOPER_ONBOARDING.md)**
- **[Architecture Decision Records (ADRs)](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/adr/README.md)**
- **[Contributing Guidelines](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/CONTRIBUTING.md)**
- **[Security Policy](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/SECURITY.md)**
