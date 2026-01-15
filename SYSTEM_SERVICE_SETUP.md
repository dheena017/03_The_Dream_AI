# 🧠 DREAM AI - SYSTEM SERVICE SETUP

## Install as System Service

To run Dream AI automatically on startup as a system service:

### Step 1: Make installer executable
```bash
chmod +x install_service.sh
```

### Step 2: Run installer with sudo
```bash
sudo bash install_service.sh
```

This will:
- ✅ Copy the service file to `/etc/systemd/system/`
- ✅ Reload the systemd daemon
- ✅ Enable Dream AI to start on boot
- ✅ Start the service immediately

---

## Manage the Service

### Check Status
```bash
sudo systemctl status dream-ai
```

### Start/Stop/Restart
```bash
sudo systemctl start dream-ai      # Start the service
sudo systemctl stop dream-ai       # Stop the service
sudo systemctl restart dream-ai    # Restart the service
```

### View Live Logs
```bash
sudo journalctl -u dream-ai -f
```

### View Service Logs (Last 50 lines)
```bash
sudo journalctl -u dream-ai -n 50
```

### Enable/Disable on Boot
```bash
sudo systemctl enable dream-ai     # Run on startup
sudo systemctl disable dream-ai    # Don't run on startup
```

### Remove Service
```bash
sudo systemctl stop dream-ai
sudo systemctl disable dream-ai
sudo rm /etc/systemd/system/dream-ai.service
sudo systemctl daemon-reload
```

---

## What the Service Does

- **Automatically starts** when system boots
- **Runs in background** (no terminal needed)
- **Auto-restarts** if it crashes
- **Logs output** to system journal
- **Manages processes** (Brain + Eyes)

---

## After Installation

Your Dream AI will:
1. ✅ Start automatically on system boot
2. ✅ Keep running in the background
3. ✅ Continue learning and observing
4. ✅ Be manageable via `systemctl` commands
5. ✅ Log to system journal (viewable via `journalctl`)

---

## Service File Details

**Location:** `/etc/systemd/system/dream-ai.service`

**Configuration:**
- **Type:** Simple (foreground process)
- **User:** dheena
- **Working Directory:** `/home/dheena/My_Life_Work/03_The_Dream_AI`
- **Restart:** Always (will restart on failure)
- **Start Script:** `start_dream_ai.sh`

---

## Quick Commands Reference

```bash
# Check if running
systemctl is-active dream-ai

# Check if enabled on boot
systemctl is-enabled dream-ai

# Show recent logs (30 lines)
journalctl -u dream-ai -n 30 --no-pager

# Stream logs in real-time
journalctl -u dream-ai -f

# Show service details
systemctl show dream-ai
```

---

## Troubleshooting

### Service won't start
```bash
# Check for errors
journalctl -u dream-ai -n 100

# Make sure scripts are executable
chmod +x start_dream_ai.sh
```

### Permission denied
```bash
# Make sure you're using sudo
sudo systemctl start dream-ai

# Check file permissions
ls -l start_dream_ai.sh
ls -l brain/bridge.py
```

### Want to see output?
```bash
# View live logs while service runs
sudo journalctl -u dream-ai -f
```

---

**🎯 Your Dream AI is now a system service!** 🧠✨
