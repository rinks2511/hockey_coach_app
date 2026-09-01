#!/usr/bin/env bash
# deployment/deploy_cloudrun.sh
# Automates building and deploying the container to Google Cloud Run

set -euo pipefail

# Configuration variables
PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "GCP_PROJECT_ID")
SERVICE_NAME="hockey-coach-app"
REGION="europe-west4" # Choose your preferred GCP region

echo "--------------------------------------------------------"
echo "Deploying ${SERVICE_NAME} to Google Cloud Run"
echo "GCP Project: ${PROJECT_ID}"
echo "GCP Region:  ${REGION}"
echo "--------------------------------------------------------"

# 1. Build and Deploy container to Cloud Run
echo "🚀 Building and deploying directly to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
  --source . \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --project "${PROJECT_ID}"

echo "✅ Deployment finished successfully!"
