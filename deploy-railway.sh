#!/bin/bash

echo "🚀 Deploying RiceResearchFinder Backend to Railway"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
    echo "✅ Railway CLI installed"
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Deploy project
echo "📦 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Your backend is now running on Railway"
echo "💡 Get your service URL from Railway dashboard"
