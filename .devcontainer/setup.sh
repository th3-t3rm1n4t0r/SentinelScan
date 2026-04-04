#!/bin/bash
set -e

echo "🚀 Initializing SentinelScan Security Environment..."

# 1. Update and install core system utilities
sudo apt-get update && sudo apt-get install -y jq httpie build-essential

# 2. Install Python dependencies for the Regex Engine
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install re2 requests python-dotenv
fi

# 3. Install Node dependencies for the Dashboard
if [ -f "package.json" ]; then
    npm install
fi

echo "✅ SentinelScan Environment Ready. Ports 5678 (n8n) and 3000 (React) are open."
touch .setup_complete
