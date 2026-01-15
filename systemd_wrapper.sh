#!/bin/bash
# Dream AI - Systemd Service Wrapper
# This keeps the service running while the background processes work

PROJECT_ROOT="/home/dheena/My_Life_Work/03_The_Dream_AI"

# Run the startup script
"$PROJECT_ROOT/start_dream_ai.sh"

# Extract PIDs from log output and keep monitoring
# This keeps systemd from thinking the service crashed
while true; do
    # Check if brain is running
    if ! pgrep -f "python3.*bridge.py" > /dev/null; then
        # If brain crashed, restart
        echo "Brain died, restarting..."
        cd "$PROJECT_ROOT/brain"
        nohup python3 bridge.py > brain.log 2>&1 &
    fi
    
    # Check if eyes is running
    if ! pgrep -f "python3.*coordinator.py" > /dev/null; then
        # If eyes crashed, restart
        echo "Eyes died, restarting..."
        cd "$PROJECT_ROOT"
        nohup python3 eyes/coordinator.py > eyes.log 2>&1 &
    fi
    
    # Sleep briefly
    sleep 10
done
