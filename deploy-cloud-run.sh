#!/bin/bash

# Google Cloud Run deployment script for REST API

set -e

# Configuration
PROJECT_ID=${PROJECT_ID:-"your-project-id"}
SERVICE_NAME="rest-api"
REGION=${REGION:-"us-central1"}
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying REST API to Google Cloud Run"
echo "=========================================="
echo "Project ID: $PROJECT_ID"
echo "Service Name: $SERVICE_NAME"
echo "Region: $REGION"
echo "Image: $IMAGE_NAME"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with gcloud. Please run:"
    echo "   gcloud auth login"
    exit 1
fi

# Set the project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and push the image
echo "🏗️  Building and pushing Docker image..."
gcloud builds submit --tag $IMAGE_NAME .

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --concurrency 100 \
    --timeout 300 \
    --set-env-vars PORT=8080,FLASK_ENV=production

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo ""
echo "✅ Deployment completed successfully!"
echo "🌐 Service URL: $SERVICE_URL"
echo ""
echo "🧪 Testing the deployment..."
echo "Home endpoint: $SERVICE_URL/"
echo "Users API: $SERVICE_URL/api/users/"
echo "Posts API: $SERVICE_URL/api/posts/"
echo ""

# Test the deployment
echo "Testing home endpoint..."
if curl -s -f "$SERVICE_URL/" > /dev/null; then
    echo "✅ Home endpoint is working"
else
    echo "❌ Home endpoint failed"
fi

echo "Testing users endpoint..."
if curl -s -f "$SERVICE_URL/api/users/" > /dev/null; then
    echo "✅ Users endpoint is working"
else
    echo "❌ Users endpoint failed"
fi

echo ""
echo "🎉 REST API is now live on Google Cloud Run!"
echo "📊 View logs: gcloud logs tail --follow --service=$SERVICE_NAME"
echo "🛑 Delete service: gcloud run services delete $SERVICE_NAME --region $REGION"
