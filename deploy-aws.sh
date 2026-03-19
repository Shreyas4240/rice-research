#!/bin/bash

echo "🚀 Deploying RiceResearchFinder Backend to AWS App Runner"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Installing..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm awscliv2.zip
    echo "✅ AWS CLI installed"
fi

# Check if App Runner CLI is installed
if ! command -v aws apprunner &> /dev/null; then
    echo "❌ AWS App Runner plugin not found. Installing..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm awscliv2.zip
    echo "✅ AWS App Runner plugin installed"
fi

# Login to AWS (if not already logged in)
echo "🔐 Checking AWS authentication..."
aws sts get-caller-identity &> /dev/null || {
    echo "❌ Not logged in to AWS. Please run: aws configure"
    exit 1
}

echo "✅ AWS authentication confirmed"

# Set variables
SERVICE_NAME="rice-research-finder-backend"
REGION="us-east-1"

echo "📦 Creating App Runner service..."
# Create a simpler service first
aws apprunner create-service \
    --service-name $SERVICE_NAME \
    --source-configuration '{
        "ImageRepository": {
            "ImageIdentifier": "public.ecr.aws/l6m2t8p7/python-fastapi:latest",
            "ImageConfiguration": {
                "Port": 8000
            },
            "RuntimeEnvironment": "PYTHON_3"
        },
        "AutoDeploymentsEnabled": true
    }' \
    --instance-configuration '{
        "Cpu": "1 vCPU",
        "Memory": "2 GB"
    }' \
    --health-check-configuration '{
        "Protocol": "HTTP",
        "Path": "/api/health",
        "Interval": 30,
        "Timeout": 5,
        "HealthyThreshold": 1,
        "UnhealthyThreshold": 3
    }' \
    --region $REGION

echo "⏳ Waiting for deployment to complete..."
# Wait for service to be running
aws apprunner wait-for-service-deployment-complete \
    --service-arn $(aws apprunner describe-service \
        --service-name $SERVICE_NAME \
        --region $REGION \
        --query 'Service.ServiceArn' \
        --output text) \
    --region $REGION

# Get the service URL
SERVICE_URL=$(aws apprunner describe-service \
    --service-name $SERVICE_NAME \
    --region $REGION \
    --query 'Service.ServiceUrl' \
    --output text)

echo "✅ Deployment complete!"
echo "🌐 Service URL: $SERVICE_URL"
echo "🔗 Health check: $SERVICE_URL/api/health"

# Update frontend API URL (optional)
echo "💡 Don't forget to update your frontend to point to: $SERVICE_URL"
echo "📝 Update ui/src/utils/api.js with the new URL"
