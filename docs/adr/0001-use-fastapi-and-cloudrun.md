# 1. Selection of FastAPI & Google Cloud Run Serverless Deployment

* **Status**: Accepted
* **Date**: 2026-09-01
* **Deciders**: Tech Lead / Architecture Team

---

## 1. Context & Problem Statement

The application requires a highly responsive, cost-effective backend system capable of managing real-time tactical board snapshots, squad rosters, parent/coach authorization, and team settings. Operations are peak-heavy during weekend matchdays, with minimal traffic during midweek training.

---

## 2. Decision Drivers

* **Sub-second Response Times**: Low latency REST endpoints for live pitch sync on mobile devices.
* **Zero Infrastructure Overhead**: Serverless execution without virtual machine maintenance or continuous compute costs.
* **Automatic Autoscaling**: Scale to zero when idle, scale up instantly during Saturday morning match windows.
* **Developer Experience**: Modern Python backend framework with native OpenAPI schema generation and standard typing.

---

## 3. Considered Options

1. **FastAPI on Google Cloud Run** *(Selected)*
2. **Django / Flask on Google Compute Engine VM**
3. **Node.js / Express on AWS Lambda**

---

## 4. Decision Outcome

**Chosen Option**: **FastAPI deployed on Google Cloud Run** (`europe-west4`).

### Positive Consequences
* Serverless containerized deployment with zero cost when idle.
* Automatic HTTPS certificate management and domain routing via Google Cloud Run.
* Sub-millisecond JSON serialization powered by Pydantic and Starlette.
* Single container standard (`Dockerfile`) ensures 100% environment parity between local Uvicorn development and cloud deployment.

### Negative Consequences
* Cold start latency (~1.5 seconds) if container scales to zero. (Mitigated by setting min-instances=0 during development and min-instances=1 on peak matchday hours if needed).
