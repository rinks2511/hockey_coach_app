# HV Myra Matchday Board Architectural Documentation Index

Welcome to the architectural and technical design documentation for the **HV Myra Matchday Board Application**. This documentation suite captures the system design decisions, data models, frontend state architecture, operational guidelines, and architectural review materials.

---

## 📚 Architectural Documentation Index

| Document | Description | Focus Areas |
| :--- | :--- | :--- |
| **[ARCHITECTURE.md](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/ARCHITECTURE.md)** | **System Architecture & Technical Design** | High-level system architecture, FastAPI router breakdown (`auth`, `config`, `tactics`, `teams`), database schema, non-destructive SQLite migrations, and Google OAuth RBAC security model. |
| **[MULTI_TENANT_DESIGN.md](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/MULTI_TENANT_DESIGN.md)** | **Multi-Tenant & Multi-Team Data Model** | `team_id` data isolation, team onboarding API (`/api/teams`), format adaptation (Youth MO10 8v8 vs Senior Trimmers 11v11), and team selector mechanics. |
| **[FRONTEND_ARCHITECTURE.md](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/FRONTEND_ARCHITECTURE.md)** | **Frontend Architecture & Refactoring Roadmap** | Global state scoping (solving ES6 Temporal Dead Zone TDZ), `window.onload` execution lifecycle, dropdown fuzzy matching, women quota validation, and React/Vite refactoring plan. |
| **[DEPLOYMENT_AND_OPERATIONS.md](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/DEPLOYMENT_AND_OPERATIONS.md)** | **Deployment, Infrastructure & Operations Guide** | Containerized Cloud Run setup (`europe-west4`), Dockerfile build spec, automated `./deployment/deploy_cloudrun.sh` script, and Local-First Quality Assurance rules. |
| **[DEVELOPER_ONBOARDING.md](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/DEVELOPER_ONBOARDING.md)** | **Developer Onboarding & Team Scaling Guide** | Quickstart local setup, test execution, step-by-step instructions for adding new teams tomorrow, and Cloud Run deployment workflow. |
| **[adr/README.md](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/adr/README.md)** | **Architecture Decision Records (ADRs)** | Formal log of architectural choices (`0001` FastAPI/CloudRun, `0002` Multi-Tenant Partitioning, `0003` Cloud SQL Migration Plan). |
| **[positions.md](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/positions.md)** | **Tactical Formations & Positions** | Reference list of pitch positions and formation configurations (`1-2-3-2`, `1-3-3-1`, `4-3-3`). |
| **[rules.md](file:///Users/rajeevsinghal/Documents/Work/projects/hockey_coach_app/docs/rules.md)** | **KNHB Hockey Rules** | Reference guide for match formats, substitution guidelines, and pitch dimensions. |
