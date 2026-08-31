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

# 1. Build and Submit the container image to Google Artifact Registry / Container Registry
echo "🚀 Building and pushing container image with Cloud Build..."
gcloud builds submit --tag "gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest" --project "${PROJECT_ID}" ..

# 2. Deploy to Cloud Run
echo "🌟 Deploying container to Cloud Run service..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --project "${PROJECT_ID}"

echo "✅ Deployment finished successfully!"
