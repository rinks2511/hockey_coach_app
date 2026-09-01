# 3. Ephemeral SQLite to Managed Cloud SQL (PostgreSQL) Migration Plan

* **Status**: Proposed / In Review
* **Date**: 2026-09-01
* **Deciders**: Infrastructure Lead / Core Team

---

## 1. Context & Problem Statement

Currently, the application uses an embedded SQLite database file (`hockey_coach.db`) written to the local filesystem of the container running on Google Cloud Run. Because Cloud Run instances are ephemeral and stateless, container restarts or multi-instance autoscaling will result in state mismatch across instances and potential data loss during revision deployments.

---

## 2. Decision Drivers

* **State Persistence & Multi-Instance Consistency**: Multiple concurrent Cloud Run instances must query and update the exact same centralized database.
* **ACID Compliance & Reliability**: High reliability for saved match sheets, attendance tracking, and tactics drawings.
* **Low Maintenance**: Managed database service with automated backups and failover.

---

## 3. Considered Options

1. **Google Cloud SQL (PostgreSQL)** *(Selected for Production)*
2. **Google Cloud Firestore / Datastore**
3. **Mounting Cloud Storage / Cloud Filestore to SQLite**

---

## 4. Migration Strategy & Roadmap

1. **Phase 1 (Current)**: Local SQLite with non-destructive table migrations (`database.py`) for local development and initial MVP deployment.
2. **Phase 2 (Database Abstraction)**: Abstract database connection factory in `database.py` using SQLAlchemy or AsyncPG to support dual engines (SQLite for dev/tests, PostgreSQL for prod).
3. **Phase 3 (Cloud SQL Setup)**: Provision Cloud SQL (PostgreSQL) instance in `europe-west4`, attach Cloud SQL Auth Proxy to Cloud Run, and set `DATABASE_URL` environment secret.
4. **Phase 4 (Data Migration)**: Export existing SQLite records to PostgreSQL seed script.

---

## 5. Consequences

* **Positive**: Full multi-instance scalability, zero data loss risks, point-in-time recovery.
* **Negative**: Introduces a small fixed monthly GCP charge for managed Cloud SQL instance (~$7-$15/month).
