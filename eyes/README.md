# 👁️ DREAM AI - EYES SYSTEM

## Overview

The Eyes System is the **observation and perception layer** of "The Digital Descendant" AI. It continuously monitors your activity across multiple dimensions and reports to the Brain for learning and analysis.

**Philosophy**: The AI learns by watching. Not from pre-trained data, but from observing how *you* work, solve problems, and think.

## Architecture

```
┌─────────────────────────────────────────────┐
│         DREAM AI - EYES SYSTEM              │
├─────────────────────────────────────────────┤
│                                             │
│  🖥️  Screen Activity Tracker                │
│      └─ Active window, app focus, changes  │
│                                             │
│  ⌨️  Input Activity Tracker                 │
│      └─ Typing patterns, idle time, mouse  │
│                                             │
│  📁 File Access Monitor                     │
│      └─ Projects, workflows, file changes  │
│                                             │
│  🌐 Browser History Capture                │
│      └─ Research topics, knowledge domains │
│                                             │
└──────────────┬──────────────────────────────┘
               │
               │ (JSON Observations)
               ▼
        🧠 BRAIN SYSTEM
       (Central Processing)
```

## Components

### 1. Screen Activity Tracker (`screen_activity.py`)

**What it sees:**
- Currently focused window/application
- Window title changes (detecting context switches)
- Display resolution and multi-monitor setup
- When you switch between apps

**Why it matters:**
- Patterns show what tools you use most
- Time spent in each application
- Problem-solving context (coding → research → design)

**Privacy:** ✓ No screenshots, no window content, only metadata

### 2. Input Activity Tracker (`input_tracker.py`)

**What it sees:**
- Keyboard activity level (idle, light, active)
- Typing intensity (estimated, not content)
- Mouse position and movement patterns
- How long you've been idle

**Why it matters:**
- When are you actively working vs. thinking?
- Are you typing code or reading documentation?
- Break patterns and focus duration

**Privacy:** ✓ No keystroke recording, no text capture

### 3. File Access Monitor (`file_monitor.py`)

**What it sees:**
- Recently modified files
- Active project directories
- File type distribution
- What applications have files open

**Why it matters:**
- Understand your project structure
- See what you're working on
- Detect workflow patterns (test → code → deploy)

**Privacy:** ✓ Only metadata, no file contents

### 4. Browser History Capture (`browser_history.py`)

**What it sees:**
- Browsing history (Firefox, Chrome, Brave, Edge)
- Domains you visit most
- Topics you research
- Search patterns

**Why it matters:**
- Understand your learning topics
- See external knowledge sources
- Track research methods

**Privacy:** ✓ No page content, only URLs and titles

### 5. Sensor Coordinator (`coordinator.py`)

**Purpose:** Central hub that:
- Orchestrates all sensors
- Collects observations in synchronized cycles
- Sends data to the Brain for processing
- Manages timing and frequency

**Usage:**
```bash
# Start the observation system
python coordinator.py

# With custom settings
DREAM_AI_INTERVAL=5 DREAM_AI_BRAIN="http://brain-server:3000/brain-log" python coordinator.py
```

## How It Works

### Observation Cycle

```
┌─────────────────────────────────┐
│  Every 10 seconds (configurable)│
└────────────┬────────────────────┘
             │
             ▼
      ┌──────────────┐
      │ Read Screen  │ ──┐
      └──────────────┘   │
      ┌──────────────┐   │
      │ Read Input   │   ├──► Combine into
      └──────────────┘   │    JSON Observation
      ┌──────────────┐   │
      │ Read Files   │   │
      └──────────────┘   │
      ┌──────────────┐   │
      │ Browser*     │   │ (*less frequent)
      └──────────────┘   │
             │            │
             └────────────┴────┐
                               │
                    ┌──────────▼──────────┐
                    │  Send to Brain via  │
                    │  HTTP POST request  │
                    └────────────────────┘
                               │
                               ▼
                    🧠 Brain processes &
                       learns from data
```

### Configuration

Set these environment variables to customize:

```bash
# How often to collect observations (seconds)
DREAM_AI_INTERVAL=10

# Brain API endpoint
DREAM_AI_BRAIN="http://localhost:3000/brain-log"

# Check browser history every N cycles
DREAM_AI_BROWSER_FREQ=6  # Every 60 seconds with 10s interval
```

## Data Format

Each observation sent to the brain looks like:

```json
{
  "observation_id": 1,
  "timestamp": "2026-01-11T14:30:45.123456",
  "sensors": {
    "screen": {
      "active_window": {
        "app_name": "code",
        "window_title": "bridge.py - VS Code",
        "window_id": "12345"
      },
      "focus_changes": []
    },
    "input": {
      "typing_intensity": "active",
      "idle_status": "active",
      "mouse": {"x": 1234, "y": 567}
    },
    "files": {
      "recent_files": [...],
      "active_projects": [...]
    },
    "browser": {
      "recent_visits": [...],
      "browsing_patterns": {...}
    }
  }
}
```

## Installation & Requirements

### System Requirements

- Python 3.8+
- Linux (with xdotool, xrandr, xprintidle)
- Supported browsers: Firefox, Chrome, Chromium, Brave, Edge

### Linux Package Installation

```bash
# Install required system tools
sudo apt-get update
sudo apt-get install -y \
    xdotool \
    xrandr \
    x11-utils \
    lsof

# For Fedora/RHEL:
# sudo dnf install xdotool xrandr lsof

# For Arch:
# sudo pacman -S xdotool xrandr lsof
```

### Python Dependencies

```bash
pip install requests
```

### Permissions

Some features may require appropriate permissions:
- File monitoring: Access to home directory and projects
- Browser history: Read access to browser profile directories
- Input tracking: Access to X11 display server

## Usage

### Start the Complete Eyes System

```bash
cd /home/dheena/My_Life_Work/03_The_Dream_AI

# Make sure the brain (server.js) is running first
node ../02_The_Capstone/backend/server.js

# In another terminal, start the eyes
python eyes/coordinator.py
```

### Test Individual Sensors

```bash
# Test all sensors
python eyes/__init__.py test

# Test specific sensor
python eyes/screen_activity.py
python eyes/input_tracker.py
python eyes/file_monitor.py
python eyes/browser_history.py
```

### Integration with Brain

The Eyes system sends observations to the Brain at the configured endpoint:

```bash
# Default: http://localhost:3000/brain-log
# The Brain receives and stores observations for analysis
```

## Observation Priorities

The system prioritizes real-time observations:

**High Priority (Every cycle):**
- Screen activity
- Input tracking
- Current idle status

**Medium Priority (Every 6 cycles ≈ 60 seconds):**
- File modifications
- Browser history
- Project changes

**Low Priority (On demand):**
- Full file system scan
- Complete history analysis

## Privacy & Security

✅ **Privacy-First Design**

1. **No Content Capture**
   - No keystroke recording
   - No screenshot saving
   - No text extraction from windows
   - No page content from browsers

2. **Metadata Only**
   - Only application names
   - Only file paths and timestamps
   - Only URLs and page titles
   - Only activity patterns

3. **Local Processing**
   - All observations processed locally
   - Data sent to Brain (also local)
   - No cloud transmission
   - No external data collection

4. **User Control**
   - Environment variables for configuration
   - Easy to stop/pause observation
   - No background services
   - Transparent operation

## Extending the Eyes System

To add new sensors:

1. Create a new Python module (e.g., `audio_monitor.py`)
2. Implement an `observe()` method returning a Dict
3. Add it to `SensorCoordinator` in `coordinator.py`
4. Update the observation cycle

Example template:

```python
class NewSensor:
    def observe(self) -> Dict:
        # Collect data
        data = {}
        # Return observation dict
        return data
```

## Troubleshooting

### Brain not responding
```
❌ Cannot connect to brain at http://localhost:3000/brain-log
   💡 Make sure server.js is running!
```

**Fix:** Start the brain first
```bash
cd /home/dheena/My_Life_Work/02_The_Capstone/backend
npm install  # if not done
node server.js
```

### xdotool not found
```
Error: xdotool command not found
```

**Fix:**
```bash
sudo apt-get install xdotool
```

### Permission denied for browser history
```
Error: Cannot access Firefox profile
```

**Fix:** Browser profiles may be in use. The system handles this gracefully and skips that observation.

## Next Steps

After Eyes are working:

1. **Brain Development** - Process and analyze observations
2. **Memory System** - Store patterns and learning
3. **Learning Engine** - Generate hypotheses about your behavior
4. **Self-Modification** - Code that improves itself

## Philosophy

> "The eyes don't make the brain. They feed it. The AI learns not from facts loaded into memory, but from patterns it observes about *how you think*."

The Eyes system is the first step in creating a true learning entity - not a tool that knows things, but an entity that *discovers* things by watching its creator.

---

**Created for Project: "The Digital Descendant"**  
**Status:** Phase 1 - Observation System ✅
