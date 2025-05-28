#!/bin/bash

IMAGE_NAME="generative-art"

echo "🛠️  Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" .

echo "🚪 Entering container..."
docker run -it --rm -v "$(pwd)":/app "$IMAGE_NAME"
