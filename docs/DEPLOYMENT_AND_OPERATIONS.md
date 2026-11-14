# Deployment, Infrastructure & Operations Guide

## 1. Overview & Cloud Architecture

The **HV Myra Matchday Board** application is deployed to **Google Cloud Run** in project `hockey-507014` (`europe-west4` region). Google Cloud Run provides serverless, containerized execution that automatically scales down to zero when idle, minimizing hosting costs while maintaining sub-second response times.

---

## 2. Infrastructure & Deployment Setup

### 2.1 Deployment Topology
- **GCP Project ID**: `hockey-507014`
- **GCP Region**: `europe-west4` (Eemshaven / Netherlands)
- **Cloud Run Service Name**: `hockey-coach-app`
- **Service URL**: `https://hockey-coach-app-1083993716124.europe-west4.run.app` (or legacy `https://hockey-coach-app-belxoh76za-ez.a.run.app`)
- **Dedicated Service Account**: `hockey-coach-app-sa@hockey-507014.iam.gserviceaccount.com` (Least-privilege: scoped to `roles/storage.objectAdmin` on `gs://hockey-507014-db-storage` and `roles/logging.logWriter`)
- **Persistent Data Volume**: GCS Bucket `hockey-507014-db-storage` mounted to `/app/data`

### 2.2 Container Build Specification (`Dockerfile`)
```dockerfile
FROM python:3.11.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt

# Copy application files
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Launch Uvicorn server
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 3. Automated Deployment Workflow (`deploy_cloudrun.sh`)

Deployments are automated via the `./deployment/deploy_cloudrun.sh` script.

### 3.1 Script Execution
```bash
# Run local tests first
PYTHONPATH=. pytest backend/tests/

# Deploy container directly to Cloud Run
./deployment/deploy_cloudrun.sh
```

### 3.2 Script Implementation (`deployment/deploy_cloudrun.sh`)
```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "hockey-507014")
SERVICE_NAME="hockey-coach-app"
REGION="europe-west4"
BUCKET_NAME="hockey-507014-db-storage"
SERVICE_ACCOUNT="hockey-coach-app-sa@${PROJECT_ID}.iam.gserviceaccount.com"

echo "--------------------------------------------------------"
echo "Deploying ${SERVICE_NAME} to Google Cloud Run"
echo "GCP Project: ${PROJECT_ID}"
echo "GCP Region:  ${REGION}"
echo "--------------------------------------------------------"

gcloud run deploy "${SERVICE_NAME}" \
  --source . \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --project "${PROJECT_ID}" \
  --service-account "${SERVICE_ACCOUNT}" \
  --add-volume "name=db-vol,type=cloud-storage,bucket=${BUCKET_NAME}" \
  --add-volume-mount "volume=db-vol,mount-path=/app/data"

echo "✅ Deployment finished successfully!"
```

---

## 4. CI/CD Security & Quality Assurance

Our GitHub Actions pipeline (`.github/workflows/deploy.yml`) runs mandatory security and quality checks on every push and pull request:

1. **Dependency CVE Auditing (`pip-audit`)**: Scans all production and dev dependencies against the PyPA and OSV vulnerability advisory databases; fails build on any known CVE.
2. **Static Application Security Testing (`bandit`)**: Performs SAST on Python backend code to detect OWASP/CWE vulnerabilities, insecure imports, and unhandled exceptions.
3. **Filesystem Vulnerability Scanning (`trivy`)**: Scans project assets and configurations for known security issues.
4. **Automated Unit Testing (`pytest`)**: Executes comprehensive multi-tenant test suites.

---

## 5. Local-First Quality Assurance Rules

To ensure production stability, developers and AI pair programmers must follow these strict operational rules:

1. **Never Deploy Unverified Code**: Run `PYTHONPATH=. pytest backend/tests/` and verify local HTTP endpoints before triggering `deploy_cloudrun.sh`.
2. **Non-Destructive Database Updates**: Never drop tables or delete volume data during migrations.
3. **Log & Traceback Inspection**: Base all bug fixes on empirical traceback evidence from server logs (`gcloud logging read` or local terminal output).
4. **Environment Consistency**: Test local behavior on `http://127.0.0.1:8085` before pushing container revisions.
