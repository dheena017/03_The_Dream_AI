#!/bin/bash
# Dream AI Quick Launcher

echo "🧠 DREAM AI - Quick Start"
echo "=========================="
echo ""

# Kill any existing processes
echo "Cleaning up old processes..."
pkill -9 -f "brain/bridge.py" 2>/dev/null
pkill -9 -f "dashboard.py" 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:5000 | xargs kill -9 2>/dev/null
sudo systemctl stop dream-ai 2>/dev/null
sleep 2

echo "✅ Cleanup complete"
echo ""

# Launch the system
echo "🚀 Launching Dream AI..."
echo ""
python3 start.py
