#!/bin/bash
# Real-time AI Activity Monitor

clear
echo "======================================"
echo "   🧠 DREAM AI - LIVE MONITOR"
echo "======================================"
echo ""

while true; do
    # Clear previous output (keep header)
    tput cup 4 0
    
    # System Status
    echo "📊 SYSTEM STATUS:"
    systemctl is-active dream-ai >/dev/null 2>&1 && echo "   ✅ Service: Running" || echo "   ❌ Service: Stopped"
    pgrep -f "bridge.py" >/dev/null && echo "   ✅ Brain: Active (PID $(pgrep -f bridge.py))" || echo "   ❌ Brain: Inactive"
    pgrep -f "coordinator.py" >/dev/null && echo "   ✅ Eyes: Active (PID $(pgrep -f coordinator.py))" || echo "   ❌ Eyes: Inactive"
    echo ""
    
    # API Status
    echo "📡 BRAIN API (port 3000):"
    STATUS=$(curl -s http://localhost:3000/status 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "   ✅ API Responding"
        echo "$STATUS" | python3 -m json.tool 2>/dev/null | head -20 || echo "$STATUS"
    else
        echo "   ❌ API Not Responding"
    fi
    echo ""
    
    # Recent Brain Activity
    echo "🧠 BRAIN ACTIVITY (last 5 lines):"
    tail -5 brain/logs/dream_ai_*.log 2>/dev/null | sed 's/^/   /' || echo "   No recent activity"
    echo ""
    
    # Memory Stats
    echo "💾 MEMORY:"
    if [ -f "brain/memory/observations.db" ]; then
        OBS=$(sqlite3 brain/memory/observations.db "SELECT COUNT(*) FROM observations;" 2>/dev/null)
        echo "   Observations: ${OBS:-0}"
    else
        echo "   Database: Not accessible"
    fi
    
    if [ -f "brain/memory/completed_tasks.json" ]; then
        TASKS=$(cat brain/memory/completed_tasks.json 2>/dev/null | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
        echo "   Completed Tasks: ${TASKS:-0}"
    fi
    echo ""
    
    # Resource Usage
    echo "⚡ RESOURCES:"
    ps aux | grep -E "bridge\.py|coordinator\.py" | grep -v grep | awk '{printf "   %s: CPU=%s%% MEM=%s%%\n", $11, $3, $4}'
    echo ""
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Press Ctrl+C to exit | Refreshing in 3s..."
    
    sleep 3
done
