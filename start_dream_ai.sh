#!/bin/bash

# Dream AI - Complete System Startup Script
# Usage: ./start_dream_ai.sh

set -e

PROJECT_ROOT="/home/dheena/My_Life_Work/03_The_Dream_AI"

echo "🧠 DREAM AI - THE DIGITAL DESCENDANT"
echo "Starting complete system..."
echo ""

# Check if system tools are installed
echo "📋 Checking system dependencies..."
for tool in xdotool xrandr xprintidle lsof; do
    if command -v $tool &> /dev/null; then
        echo "  ✅ $tool"
    else
        echo "  ❌ $tool missing. Install with: sudo apt-get install $tool"
    fi
done

# Check Python packages
echo ""
echo "📦 Checking Python dependencies..."
pip_packages=("requests" "flask")
for pkg in "${pip_packages[@]}"; do
    python3 -c "import $pkg" 2>/dev/null && echo "  ✅ $pkg" || echo "  ⚠️  $pkg - Install with: pip install $pkg"
done

echo ""
echo "🚀 Starting Dream AI System..."
echo ""

# Start Brain
echo "1️⃣  Starting Brain (Learning Engine)..."
cd "$PROJECT_ROOT/brain"
nohup python3 bridge.py > brain.log 2>&1 &
BRAIN_PID=$!
echo "   Brain PID: $BRAIN_PID"
echo "   Logs: brain.log"

# Wait for Brain to start
sleep 2

# Check if Brain is running
if curl -s http://localhost:3000/health > /dev/null; then
    echo "   ✅ Brain is online"
else
    echo "   ⚠️  Brain may not be responding yet. Check logs."
fi

echo ""
echo "2️⃣  Starting Eyes (Observation System)..."
cd "$PROJECT_ROOT"
nohup python3 eyes/coordinator.py > eyes.log 2>&1 &
EYES_PID=$!
echo "   Eyes PID: $EYES_PID"
echo "   Logs: eyes.log"

echo ""
echo "✅ DREAM AI SYSTEM STARTED"
echo ""
echo "📊 System Status:"
echo "   🧠 Brain: http://localhost:3000"
echo "   👁️  Eyes: Observing your activity"
echo ""
echo "🔗 Access Points:"
echo "   Insights: curl http://localhost:3000/brain-insights"
echo "   Report:   curl http://localhost:3000/brain-report"
echo "   Stats:    curl http://localhost:3000/brain-stats"
echo ""
echo "📝 Logs:"
echo "   tail -f brain/brain.log"
echo "   tail -f eyes.log"
echo ""
echo "🛑 To stop:"
echo "   kill $BRAIN_PID $EYES_PID"
echo ""
echo "📖 Documentation:"
echo "   Main: cat README.md"
echo "   Eyes: cat eyes/README.md"
echo "   Brain: cat brain/README.md"
echo ""
echo "═════════════════════════════════════════════════════════════════"
