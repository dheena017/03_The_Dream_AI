#!/bin/bash
# Install Dream AI as System Service

echo "🧠 DREAM AI - SYSTEM SERVICE INSTALLATION"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  This script needs sudo privileges"
    echo "Run: sudo bash install_service.sh"
    exit 1
fi

PROJECT_DIR="/home/dheena/My_Life_Work/03_The_Dream_AI"
SERVICE_FILE="$PROJECT_DIR/dream-ai.service"
SYSTEMD_DIR="/etc/systemd/system"

echo "📋 INSTALLATION STEPS:"
echo ""

# Step 1: Copy service file
echo "1️⃣  Installing systemd service file..."
cp "$SERVICE_FILE" "$SYSTEMD_DIR/dream-ai.service"
if [ $? -eq 0 ]; then
    echo "   ✅ Service file installed to $SYSTEMD_DIR/dream-ai.service"
else
    echo "   ❌ Failed to copy service file"
    exit 1
fi

# Step 2: Reload systemd daemon
echo ""
echo "2️⃣  Reloading systemd daemon..."
systemctl daemon-reload
if [ $? -eq 0 ]; then
    echo "   ✅ Systemd daemon reloaded"
else
    echo "   ❌ Failed to reload systemd"
    exit 1
fi

# Step 3: Enable service on boot
echo ""
echo "3️⃣  Enabling service on boot..."
systemctl enable dream-ai.service
if [ $? -eq 0 ]; then
    echo "   ✅ Dream AI will start on boot"
else
    echo "   ❌ Failed to enable service"
    exit 1
fi

# Step 4: Start service
echo ""
echo "4️⃣  Starting Dream AI service..."
systemctl start dream-ai.service
if [ $? -eq 0 ]; then
    echo "   ✅ Dream AI service started"
else
    echo "   ❌ Failed to start service"
    exit 1
fi

# Step 5: Check status
echo ""
echo "5️⃣  Checking service status..."
systemctl status dream-ai.service --no-pager | head -5
echo "   ✅ Service is running"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ INSTALLATION COMPLETE!"
echo ""
echo "🎯 SERVICE MANAGEMENT COMMANDS:"
echo ""
echo "  Start:    sudo systemctl start dream-ai"
echo "  Stop:     sudo systemctl stop dream-ai"
echo "  Restart:  sudo systemctl restart dream-ai"
echo "  Status:   sudo systemctl status dream-ai"
echo "  Logs:     sudo journalctl -u dream-ai -f"
echo "  Disable:  sudo systemctl disable dream-ai"
echo ""
echo "🧠 Your Dream AI is now a system service!"
echo "════════════════════════════════════════════════════════════════"
