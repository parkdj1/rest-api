#!/bin/bash

# Docker deployment script for REST API

set -e

echo "🐳 Building Docker image for REST API..."

# Build the Docker image
docker build -t rest-api:latest .

echo "✅ Docker image built successfully!"

# Check if container is already running
if [ "$(docker ps -q -f name=rest-api)" ]; then
    echo "🔄 Stopping existing container..."
    docker stop rest-api
    docker rm rest-api
fi

# Run the container
echo "🚀 Starting REST API container..."
docker run -d \
    --name rest-api \
    -p 8000:8000 \
    -e PORT=8000 \
    -e FLASK_ENV=production \
    rest-api:latest

echo "✅ REST API is now running!"
echo "🌐 API available at: http://localhost:8000"
echo "📊 Health check: http://localhost:8000/"

# Show container status
echo ""
echo "📋 Container status:"
docker ps -f name=rest-api

echo ""
echo "📝 To view logs: docker logs rest-api"
echo "🛑 To stop: docker stop rest-api"
echo "🗑️  To remove: docker rm rest-api"
