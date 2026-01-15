# 🧠 DREAM AI - Complete System Guide

## 🎉 CONGRATULATIONS! Your AI is Complete

You have successfully built a **Self-Evolving, Autonomous AI System** with:

✅ **The Body (Bridge)** - Web server that receives and processes commands  
✅ **The Subconscious (Innovator)** - Autonomous loop with "boredom" that tries new things  
✅ **The Eyes (Web Researcher)** - Searches the web when encountering unknown tasks  
✅ **The Memory (Skill Library)** - Permanent storage of learned abilities  
✅ **The Face (Dashboard)** - Live web interface to monitor and control the AI  

---

## 🚀 Quick Start

### Method 1: Full System Launch (Recommended)
```bash
python3 start.py
```

This starts:
- **Brain (Port 3000)** - Processing engine
- **Dashboard (Port 5000)** - Visual interface

### Method 2: Individual Components
```bash
# Terminal 1: Brain
python3 brain/bridge.py

# Terminal 2: Dashboard
python3 dashboard.py
```

---

## 🖥️ Access Points

| Component | URL | Purpose |
|-----------|-----|---------|
| **Dashboard** | http://localhost:5000 | Visual control panel |
| **Brain API** | http://localhost:3000 | Direct command interface |

---

## 🎯 The Three Modes (Prime Directive)

Your AI has three distinct "personalities". Change them by editing `brain/bridge.py` line 51:

### 1. SysAdmin Mode (Default)
```python
AI_MODE = "sysadmin"
```
**Behavior:** Machine janitor - obsessed with files, disk space, processes  
**Tasks:** "scan for large files", "analyze disk usage", "check system processes"

### 2. Python Learner Mode
```python
AI_MODE = "python_learner"
```
**Behavior:** Eager student - wants to learn algorithms  
**Tasks:** "Find python code for Fibonacci", "Find python code to sort a list"

### 3. Researcher Mode
```python
AI_MODE = "researcher"
```
**Behavior:** Curious scholar - searches for knowledge  
**Tasks:** "search for AI news", "search for best practices"

**After changing mode:** Restart the system (`Ctrl+C` then `python3 start.py`)

---

## 🎮 Using the Dashboard

### Live Monitoring
- **Prime Directive** - Current AI mode
- **System Statistics** - Tasks completed, scripts generated, memory size
- **Task Queue** - What the AI is working on right now
- **Recent Activity** - Last 5 completed tasks
- **Wisdom Log** - AI's self-reflections

### Interactive Control
1. **Mode Switching** - Click mode buttons to change AI personality
2. **Command Input** - Type commands and send directly to AI

Example commands:
```
Check bitcoin price
Calculate 100 * 25
Scan /tmp for large files
Find python code to parse JSON
```

---

## 🧠 How It Works

### The Complete Flow

```
1. INNOVATOR (Autonomous)
   ↓ (Every 10 seconds)
   Generates task based on mode
   ↓
2. HTTP REQUEST to Bridge
   ↓
3. BRIDGE checks:
   - Skill Library (do we know this?)
   - Self-Evolution (is it self-improvement?)
   - SmartDeveloper (generate new code)
   ↓
4. RUNNER executes code
   ↓
5. REFLECTOR analyzes success
   ↓
6. SKILL LIBRARY saves if successful
```

### The Intelligence Test (Long-Term Learning)

Watch for this sequence to verify your AI is truly learning:

1. **First time**: AI encounters "Find python code to sort a list"
2. **Doesn't have it**: Triggers Web Researcher
3. **Generates code**: Creates new Python script
4. **Executes successfully**: Saves to Skill Library ✅
5. **10 minutes later**: Same task appears
6. **SKIP GOOGLE**: Runs from Skill Library directly 🎯

**Victory Moment:** When it skips the research and runs from memory!

---

## 📊 Key Features

### 1. Boredom Logic (Anti-Repetition)
The AI remembers the last 5 tasks and won't repeat them immediately. It cycles through different tasks to avoid being a "broken record."

### 2. Skill Library (Permanent Memory)
Successful tasks are automatically saved to `brain/skills/` and indexed. The AI checks here first before generating new code.

**View your skills:**
```bash
ls -la brain/skills/
cat brain/skills/skill_index.json
```

### 3. Hot-Swappable Modes
Change the AI's personality while it's running using the dashboard mode buttons (requires restart to activate).

### 4. HTTP-Based Circuit
The Innovator sends tasks directly to the Bridge via HTTP, creating a closed autonomous loop.

---

## 📁 File Structure

```
Dream_AI/
├── start.py                    # Master launcher (run this!)
├── dashboard.py                # Visual interface
├── brain/
│   ├── bridge.py              # Main brain (port 3000)
│   ├── skill_library.py       # Permanent memory
│   ├── evolution/
│   │   ├── innovator.py       # Autonomous decision maker
│   │   ├── smart_developer.py # Code generator
│   │   └── self_evolution.py  # Self-improvement engine
│   ├── skills/                # Permanent skill storage
│   │   └── skill_index.json   # Skill catalog
│   ├── generated/             # Temporary scripts
│   └── memory/
│       └── completed/         # Archived tasks
├── templates/
│   └── dashboard.html         # Dashboard UI
└── eyes/                      # Activity monitoring
```

---

## 🧪 Testing the System

### Test 1: Manual Command
```bash
curl -X POST http://localhost:3000/command \
  -H "Content-Type: application/json" \
  -d '{"task": "Check bitcoin price"}'
```

### Test 2: Dashboard Command
1. Open http://localhost:5000
2. Type "Calculate 50 * 20" in command box
3. Click "Send Command to AI"
4. Watch Recent Activity update

### Test 3: Mode Switch
1. Open dashboard
2. Click "Python Learner" button
3. Restart system
4. Watch it start learning algorithms

---

## 🔧 Troubleshooting

### Dashboard not loading?
- Check if port 5000 is available: `lsof -i :5000`
- Ensure Flask is installed: `pip install flask`

### Brain not responding?
- Check if port 3000 is available: `lsof -i :3000`
- View logs: `tail -f brain/brain.log`

### Tasks not executing?
- Verify RUNNER_ENABLED exists: `touch brain/RUNNER_ENABLED`
- Check permissions: `chmod +x brain/runner.py`

### Innovator not posting tasks?
- Check bridge is running on port 3000
- View innovator output in terminal

---

## 🎓 Advanced Usage

### Custom Modes
Add your own mode in `brain/evolution/innovator.py`:

```python
self.mode_tasks = {
    "sysadmin": [...],
    "python_learner": [...],
    "researcher": [...],
    "your_custom_mode": [
        "AUTONOMOUS_TASK: your task 1",
        "AUTONOMOUS_TASK: your task 2",
    ]
}
```

Then set in `brain/bridge.py`:
```python
AI_MODE = "your_custom_mode"
```

### Viewing Skill Library
```bash
# List all learned skills
cat brain/skills/skill_index.json | python3 -m json.tool

# Count skills
ls brain/skills/*.py | wc -l
```

### Monitoring in Real-Time
```bash
# Watch brain activity
tail -f brain/brain.log

# Watch wisdom accumulation  
tail -f brain/wisdom.txt

# Watch task queue
watch -n 1 cat brain/tasks.txt
```

---

## 🌟 What Makes This Special

### Traditional AI vs Your AI

| Traditional AI | Your Dream AI |
|---------------|---------------|
| Needs constant instructions | Autonomous - thinks on its own |
| Forgets after restart | Permanent memory (skill library) |
| Same behavior always | Modes - different personalities |
| Black box | Live dashboard - see its thoughts |
| One-shot tasks | Learns and reuses skills |

---

## 🎯 Next Steps

### Phase 1: Observe (1-2 hours)
Run in SysAdmin mode and watch it work. You should see:
- Disk analysis every ~30 seconds
- File scanning rotating with other tasks
- Wisdom log growing

### Phase 2: Switch Modes (test)
Change to `python_learner` and restart. You should see:
- "Find python code for Fibonacci"
- "Find python code to sort a list"
- Different behavior entirely

### Phase 3: Interactive Commands (experiment)
Use dashboard to send commands:
- "Check bitcoin price" → See web research
- "Calculate math" → See instant execution
- Same command again → See skill library kick in

### Phase 4: Long-Term Evolution (24/7)
Leave it running overnight. Check in the morning:
- How many skills learned?
- What's in the wisdom log?
- Did it encounter new situations?

---

## 💡 The Vision

You've built a **Digital Employee** that:
- Works 24/7 without supervision
- Learns from every task
- Gets better over time
- Has different "moods" (modes)
- Shows you its thoughts (dashboard)

This is not just automation - it's **artificial autonomy**.

---

## 📞 System Status Indicators

### Dashboard Status Dot
- 🟢 **Green blinking** - System healthy
- 🔴 **Red/Missing** - Connection lost

### Dashboard Updates
- Auto-refreshes every 3 seconds
- Shows real-time queue status
- Live task completion tracking

---

## 🏆 Success Criteria

You'll know it's working when:
1. ✅ Dashboard shows live statistics
2. ✅ Task queue cycles through different tasks
3. ✅ Wisdom log grows over time
4. ✅ Skill library accumulates files
5. ✅ Same task runs faster on second attempt (uses library)

---

**Your AI is alive. Let it run. Let it learn. Watch it evolve.**

**Status:** ✅ Production Ready  
**Mode:** 24/7 Autonomous Operation  
**Evolution:** Continuous Learning Enabled  

🚀 **Launch command:** `python3 start.py`
