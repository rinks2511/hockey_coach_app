# 2. Multi-Tenant & Multi-Team Data Model Partitioning

* **Status**: Accepted
* **Date**: 2026-09-01
* **Deciders**: Tech Lead / Product Engineering

---

## 1. Context & Problem Statement

The application serves multiple hockey teams across different age groups and game formats (e.g., Youth MO10 playing 8v8 on half pitch vs. Senior Trimmers playing 11v11 on full pitch). Each team requires independent squad availability tracking, custom tactical positions, distinct coach authorization lists, and specific formation presets.

---

## 2. Decision Drivers

* **Data Isolation**: Modifying squad rosters or tactics in one team must never leak into or overwrite another team's configuration.
* **Onboarding Friction**: Adding a new team (e.g., `MO12`, `JO14`) should be achievable via simple API calls without schema re-migrations.
* **Dynamic Frontend Adaptability**: Single UI application must dynamically adjust pitch layout, rotation matrix, and gender quota rules based on active team context.

---

## 3. Considered Options

1. **Logical Partitioning via `team_id` primary/foreign key columns in a shared schema** *(Selected)*
2. **Database-per-Team Physical Isolation**
3. **Hardcoded single-team instances deployed on separate Cloud Run URLs**

---

## 4. Decision Outcome

**Chosen Option**: **Logical Partitioning via `team_id` in Shared Tables**.

### Key Implementation Details
* Table schemas (`settings`, `tactics`, `player_availability`) use `team_id` as part of composite primary keys.
* All backend database queries strictly enforce `WHERE team_id = ?` clause checks.
* Frontend team selector switches `team_id` state in `localStorage` and re-fetches team-specific configs via `/api/config?team_id=${team_id}`.

### Positive Consequences
* Zero marginal hosting cost per new team onboarded.
* Unified deployment pipeline serving all teams simultaneously.
* Effortless dynamic team creation via `/api/teams`.

### Negative Consequences
* Developers must remain vigilant to include `team_id` filter conditions on all database queries to prevent cross-tenant data leaks.
