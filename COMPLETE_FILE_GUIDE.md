# 🧠 DREAM AI - COMPLETE FILE GUIDE

## ROOT LEVEL FILES (Project Management)
```
├── README.md                      # Main project documentation
├── requirements.txt               # Python dependencies
├── dream-ai.service              # Systemd service configuration
├── systemd_wrapper.sh            # Process monitoring wrapper
├── start_dream_ai.sh             # Main startup script
├── install_service.sh            # Service installation script
├── SYSTEM_SERVICE_SETUP.md       # Service setup documentation
├── test_ai.py                    # Comprehensive Python test suite
├── test_dream_ai.sh              # Quick bash tests
├── test_intelligence.sh          # Intelligence capability tests
├── watch_ai.sh                   # Real-time activity monitor
├── TESTING_GUIDE.md              # Complete testing documentation
└── eyes.log, brain.log           # Live activity logs
```

---

## 🧠 BRAIN SYSTEM (Learning Engine - Port 3000)
### Core Components:

**bridge.py** - THE MAIN CONTROLLER
- Connects Eyes (observation) to Brain (learning)
- REST API endpoints (/command, /status, /brain-log)
- Integrates SmartDeveloper for code generation
- Executes tasks via Runner
- Status: ✅ ACTIVE

**orchestrator.py** - Brain Orchestration
- Processes observations
- Manages learning patterns
- Coordinates between modules
- Insight generation

**memory.py** - Long-term Storage
- SQLite observations database
- Persistent learning across sessions
- 146+ observations stored
- 23 unique applications tracked
- 58+ unique files monitored

**observation_memory.py** - Observation Handler
- Stores observation events
- Retrieves historical data
- Pattern matching from memory

### Learning & Analysis:

**activity_analyzer.py** - Tracks user patterns
**workflow_analyzer.py** - Analyzes workflows
**knowledge_mapper.py** - Maps knowledge relationships
**patterns.py** - Pattern recognition
**cognitive_architecture.py** - Core thinking model
**health_check.py** - System health monitoring
**immune_system.py** - Error recovery

### Evolution & Self-Improvement:

**evolution/** (22 files)
- **smart_developer.py** - Code generation engine
  - Math calculations
  - Google searches
  - System maintenance
  - Fallback responses
- **code_analyzer.py** - Analyzes generated code
- **code_templates.py** - Code templates library
- **confidence_calculator.py** - Evaluates solution quality
- **improvement_generator.py** - Suggests improvements
- **self_modifier.py** - Self-modification capability
- Plus 16 more specialized modules

### Memory Organization:

**memory/** (Persistent Storage)
- `observations.db` - SQLite database (146 records)
- `completed_tasks.json` - 71+ archived tasks
- `skills.json` - Learned skills registry
- `execution_log.json` - Execution history

### Generated Content:

**generated/** - Working scripts
- `task_smart_*.py` - Active task scripts
- Automatically executed by Runner
- Cleaned up after execution

**brain/brain/memory/completed/** - Archived Scripts
- Executed and archived tasks
- Preserved for learning
- 11+ completed task records

### Storage:

**wisdom.txt** - Extracted insights and DATA tags
**tasks.txt** - Task inbox
**search_results_*.txt** - Search output files
**brain.log** - Activity log

### Configuration Flags:

**RUNNER_ENABLED** - Enables auto-execution of tasks
**AUTONOMOUS_ENABLED** - Enables autonomous learning mode
**IMMUNE_ENABLED** - Enables error recovery

---

## 👁️ EYES SYSTEM (Observation Engine)
### Activity Monitoring:

**coordinator.py** - Master Observer
- Orchestrates all observation modules
- Sends observations to Brain
- Status: ✅ ACTIVE

**screen_activity.py** - Visual Tracking
- Monitors screen changes
- Window title tracking
- X11/Wayland compatible

**input_tracker.py** - Input Monitoring
- Keyboard events
- Mouse movements
- User interaction patterns

**browser_history.py** - Browser Tracking
- Browser history monitoring
- URL extraction
- Tab activity tracking

**file_monitor.py** - File System Tracking
- File access monitoring
- Creation/modification tracking
- Directory monitoring

**google_search.py** - Search Activity
- Google search tracking
- Query monitoring

---

## 🔧 UTILITIES & TOOLS

**utils/sanitizer.py** - Code validation
- Python syntax checking
- Safe code execution verification

**utils/web_researcher.py** - Web research capabilities
- HTTP requests
- Data extraction

**runner.py** - Task Execution Engine
- Executes generated Python scripts
- 30-second timeout protection
- Output capture and processing
- Task archival to memory
- Status: ✅ ACTIVE

**health_check.py** - System diagnostics
- Module validation
- Directory verification
- Permission checking
- Disk space monitoring

**immune_system.py** - Error recovery
- Exception handling
- System restoration
- Crash recovery

**chat.py** - Conversation interface
**commander.py** - Command processing
**human_brain_bridge.py** - Human interaction layer
**reset_brain.py** - Memory reset utility
**upgrade_ai.py** - System upgrade tool

---

## 📊 COMPLETE SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    REST API (Port 3000)                 │
│  POST /command      - Send task to Brain                │
│  GET  /status       - Get system status                 │
│  POST /brain-log    - Log observation from Eyes         │
└─────────────────────────────────────────────────────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
          ┌──────────────────┐ ┌──────────────────┐
          │   BRIDGE.PY      │ │  ORCHESTRATOR.PY │
          │ (Ear/Interface)  │ │  (Brain Core)    │
          └──────────────────┘ └──────────────────┘
                    │             │
      ┌─────────────┼─────────────┤─────────────┐
      ▼             ▼             ▼             ▼
   EYES       MEMORY.PY    SmartDeveloper   PATTERNS.PY
 (Observer)  (Storage)    (Code Generator)  (Learning)
   │              │             │             │
   ├─ coordinator.py
   ├─ screen_activity.py        │
   ├─ input_tracker.py          │
   ├─ browser_history.py        │
   ├─ file_monitor.py           │
   └─ google_search.py          │
                                 │
                            RUNNER.PY
                          (Executor)
                            │
                    ┌───────┴───────┐
                    ▼               ▼
                Execution       Memory Archive
                Output          (Completed Tasks)
```

---

## 📈 CURRENT STATUS

### Active Processes:
- ✅ Brain (bridge.py) - PID: Running
- ✅ Eyes (coordinator.py) - PID: Running
- ✅ Service Wrapper - Monitoring

### Statistics:
- 📊 Observations: 146 total
- 📁 Applications Tracked: 23
- 📄 Files Monitored: 58+
- ✅ Completed Tasks: 11+
- 🧠 Learning Updates: 3+

### Capabilities:
- ✅ Code Generation (SmartDeveloper)
- ✅ Task Execution (Runner)
- ✅ Activity Observation (Eyes)
- ✅ Pattern Learning (Patterns)
- ✅ Memory Storage (SQLite)
- ✅ REST API (Flask)
- ✅ Auto-execution (RUNNER_ENABLED)

---

## 🚀 HOW TO USE

### Start Everything:
```bash
sudo systemctl start dream-ai
```

### Send a Command:
```bash
curl -X POST http://localhost:3000/command \
  -H "Content-Type: application/json" \
  -d '{"task": "Calculate 100 * 25"}'
```

### Check Status:
```bash
curl http://localhost:3000/status
```

### View Logs:
```bash
sudo journalctl -u dream-ai -f
```

### Monitor Live Activity:
```bash
./watch_ai.sh
```

### Run Tests:
```bash
./test_intelligence.sh
```

---

## 🔑 KEY FILES BY FUNCTION

### For Commands/Tasks:
- bridge.py → runner.py → Generated scripts

### For Observations:
- coordinator.py → activity modules → memory.py

### For Learning:
- patterns.py ← memory.py ← observations.db

### For Generation:
- SmartDeveloper → code_analyzer.py → runner.py

---

## 💾 FILE SIZES

```
Brain System: ~2.5MB (core logic)
Eyes System: ~200KB (monitoring)
Memory: ~5MB (observations + database)
Evolution: ~800KB (code generation modules)
Generated: ~50KB (active task scripts)
Logs: ~1-2MB (activity logs)
```

---

**Total System**: ~12MB (Lightweight, Efficient, Always Running)

**Last Updated**: January 15, 2026
**System Status**: ✅ FULLY OPERATIONAL
**AI Status**: 🧠 LEARNING & EVOLVING
