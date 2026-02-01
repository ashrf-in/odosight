#!/bin/bash
# OdoSight Standalone Installer
# Usage: curl -sSL https://raw.githubusercontent.com/ashrf-in/autonomous-cfo-app/master/install.sh | bash -s -- YOUR_BOT_TOKEN

TOKEN=$1

if [ -z "$TOKEN" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN is required."
    echo "Usage: ./install.sh YOUR_BOT_TOKEN"
    exit 1
fi

echo "🚀 Starting OdoSight Installation..."

# Check for Docker
if ! [ -x "$(command -v docker)" ]; then
  echo "⚠️ Docker is not installed. Please install Docker first."
  exit 1
fi

# Clone, Build, and Run
git clone https://github.com/ashrf-in/autonomous-cfo-app.git
cd autonomous-cfo-app
mkdir -p data

echo "🛠 Building Docker image..."
docker build -t odosight .

echo "🏃 Launching CFO Bot..."
docker run -d \
  --name odosight \
  --restart always \
  -e TELEGRAM_BOT_TOKEN="$TOKEN" \
  -v "$(pwd)/data:/app/data" \
  odosight

echo "✅ Done! Your OdoSight is now running in the background."
echo "📲 Go to Telegram and message your bot to start setup."
