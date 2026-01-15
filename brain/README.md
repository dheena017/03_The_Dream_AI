# 🧠 DREAM AI - BRAIN SYSTEM

## Overview

The Brain System is the **learning and analysis layer** of "The Digital Descendant" AI. It receives observations from the Eyes, stores them, analyzes patterns, and generates insights about your behavior, capabilities, and future actions.

**Philosophy**: The Brain doesn't have pre-programmed knowledge. It *learns* by analyzing what it observes.

## Architecture

```
┌─────────────────────────────────────────────┐
│     DREAM AI - BRAIN SYSTEM                 │
├─────────────────────────────────────────────┤
│                                             │
│  📦 Observation Memory                      │
│      └─ Persistent storage (SQLite)         │
│                                             │
│  🔍 Pattern Recognition                     │
│      └─ App sequences, work sessions        │
│                                             │
│  📊 Activity Analyzer                       │
│      └─ Productivity, focus, tools          │
│                                             │
│  🔧 Workflow Analyzer                       │
│      └─ Projects, development patterns      │
│                                             │
│  🗺️  Knowledge Mapper                       │
│      └─ Learning topics, research style     │
│                                             │
│  🧠 Brain Orchestrator                      │
│      └─ Unified learning & insights         │
│                                             │
└──────────────┬──────────────────────────────┘
               │
               │ (REST API)
               ▼
        💼 LEARNING REPORTS
       (What AI has learned)
```

## Components

### 1. Observation Memory (`memory.py`)

**Purpose**: Persistent storage of all observations

**Features**:
- SQLite database for structured storage
- Fast queries by time, app, file, domain
- Normalized storage for efficient analysis
- Memory statistics (total observations, unique apps, etc.)

**Key Methods**:
```python
memory = ObservationMemory()
memory.store_observation(observation_dict)
observations = memory.get_observations(limit=100, hours=24)
app_usage = memory.get_app_usage(hours=24)
stats = memory.get_memory_stats()
```

### 2. Pattern Recognition (`patterns.py`)

**Purpose**: Identify behavioral patterns and routines

**What it detects**:
- App switching sequences (e.g., "code → browser → code")
- Work sessions (continuous periods with same app)
- Learning workflows (how you solve problems)
- Predictions (what you'll do next)
- Daily rhythms (when you're most productive)

**Example Pattern**: "Every afternoon at 3pm, you switch from code editor to browser for 15 minutes, then back to coding"

### 3. Activity Analyzer (`activity_analyzer.py`)

**Purpose**: Analyze your activity metrics and productivity

**Metrics**:
- Focus time (uninterrupted work on one task)
- Productivity score (0-100 based on typing, focus, consistency)
- Tool categorization (editors, terminals, browsers, etc.)
- Productivity trends (comparing time periods)

**Productivity Score Formula**:
- 40% typing ratio (active work vs idle)
- 40% focus duration (ability to stay on task)
- 20% consistency (regularity of activity)

### 4. Workflow Analyzer (`workflow_analyzer.py`)

**Purpose**: Understand your development workflows

**Analyzes**:
- Active projects and their status
- Coding workflow (edit → test → deploy)
- Development patterns (peak coding hours)
- File modification patterns
- Project structure understanding

### 5. Knowledge Mapper (`knowledge_mapper.py`)

**Purpose**: Map your learning and knowledge acquisition

**Tracks**:
- Research topics and domains
- Learning style (video, documentation, hands-on, searching)
- Knowledge acquisition velocity
- Topic connections (what you learn together)
- Learning intensity (research vs building)

**Learning Styles Detected**:
- 📺 Visual: Video tutorials (YouTube, Skillshare)
- 📖 Detail-oriented: Documentation reading
- 🛠️ Practical: Hands-on coding (GitHub, examples)
- 🔍 Problem-solver: Search-driven learning (StackOverflow)

### 6. Brain Orchestrator (`orchestrator.py`)

**Purpose**: Central brain that coordinates all analysis

**Generates**:
- Comprehensive analysis of all patterns
- Self-report (what AI knows about you and itself)
- High-level insights
- Recommendations
- Behavior predictions

**Key Methods**:
```python
brain = BrainOrchestrator()
brain.process_observation(observation)
report = brain.generate_self_report()
analysis = brain.generate_full_analysis()
brain.display_summary()
```

### 7. Bridge (`bridge.py`)

**Purpose**: Neural connection between Eyes and Brain

**Functions**:
- Receives observations via HTTP
- Processes them through Brain
- Exposes learning API

**Endpoints**:
- `POST /brain-log` - Receive observations from Eyes
- `GET /brain-report` - Get learning report
- `GET /brain-stats` - Get statistics
- `GET /brain-insights` - Get current insights
- `GET /health` - Health check

## How Learning Works

### 1. Observation Storage

```
Eyes capture screenshot → Coordinator packages JSON → HTTP POST → Bridge
                                                                      ↓
                                                          Store in SQLite Memory
```

### 2. Pattern Recognition

```
Stored Observation
       ↓
Read from Memory (100+ observations)
       ↓
Extract Patterns:
  - App sequences
  - Work sessions
  - Time patterns
       ↓
Generate Insights:
  - "You work in 2-hour chunks"
  - "You switch to browser for research"
  - "Most productive 10am-12pm"
```

### 3. Behavior Analysis

```
Timeline Data (24h)
       ↓
Calculate Metrics:
  - Productivity Score
  - Focus Duration
  - Typing Intensity
       ↓
Compare Trends:
  - vs. Last Week
  - vs. Monthly Average
       ↓
Generate Report:
  - "Productivity up 15% this week"
  - "Average focus doubled"
```

### 4. Learning Generation

```
All Analyses
    ↓
Orchestrator Combines:
  - Patterns
  - Activity metrics
  - Workflows
  - Knowledge map
    ↓
Creates Self-Knowledge:
  - "I am most productive mornings"
  - "I learn by hands-on coding"
  - "My typical workflow is..."
    ↓
Generates Insights:
  - Recommendations
  - Predictions
  - Self-awareness statements
```

## Data Schema

### observations table
```sql
CREATE TABLE observations (
    id INTEGER PRIMARY KEY,
    observation_id INTEGER UNIQUE,
    timestamp TEXT,
    raw_data TEXT,  -- Full JSON
    created_at DATETIME
);
```

### screen_activity table
```sql
CREATE TABLE screen_activity (
    observation_id INTEGER,
    app_name TEXT,
    window_title TEXT,
    timestamp TEXT
);
```

### input_activity table
```sql
CREATE TABLE input_activity (
    observation_id INTEGER,
    typing_intensity TEXT,  -- 'idle', 'light', 'active'
    idle_status TEXT,
    idle_seconds REAL
);
```

### file_activity table
```sql
CREATE TABLE file_activity (
    observation_id INTEGER,
    file_path TEXT,
    file_extension TEXT,
    file_size INTEGER
);
```

### browser_activity table
```sql
CREATE TABLE browser_activity (
    observation_id INTEGER,
    domain TEXT,
    page_title TEXT,
    url TEXT
);
```

## Running the Brain

### Start the Bridge/Brain Server

```bash
cd /home/dheena/My_Life_Work/03_The_Dream_AI/brain
pip install flask  # If not already installed
python bridge.py
```

The Brain will:
- Start HTTP server on `http://localhost:3000`
- Listen for observations from Eyes
- Process and store them
- Expose learning API

### Generate Analysis Report

```bash
cd /home/dheena/My_Life_Work/03_The_Dream_AI/brain
python orchestrator.py
```

This will:
- Load all stored observations
- Run complete analysis
- Generate self-report
- Save report to JSON file
- Display summary

### Quick Analysis

```bash
cd /home/dheena/My_Life_Work/03_The_Dream_AI/brain
python __init__.py analyze
```

## Using the API

### Check Health

```bash
curl http://localhost:3000/health
```

### Get Brain Insights

```bash
curl http://localhost:3000/brain-insights | jq .
```

### Get Statistics

```bash
curl http://localhost:3000/brain-stats | jq .
```

### Get Full Report

```bash
curl http://localhost:3000/brain-report | jq . > report.json
```

## Output Examples

### Productivity Score Report
```json
{
  "overall_productivity_score": 72.5,
  "typing_ratio": 65.3,
  "focus_score": 78.2,
  "consistency_score": 71.0
}
```

### Insights Generated
```
1. Productivity: Your productivity score is 72.5/100
   - Typing ratio: 65.3%, Focus score: 78.2%

2. Focus Area: Your primary focus is Web Development
   - Top tools: VS Code, Python, Node.js

3. Learning Style: You're a practical learner
   - You learn by building and experimenting

4. Work Pattern: Your typical workflow: code → browser → code
   - Observed 47 times this week

5. Focus Potential: Average focus session: 23 minutes
   - Longest session: 142 minutes
```

### Self-Report Example
```json
{
  "about_you": {
    "productivity_level": 72.5,
    "primary_activities": ["Web Development", "Data Analysis"],
    "learning_style": "hands_on_coding",
    "active_projects": 3,
    "research_focus": ["machine learning", "react", "python"]
  },
  "about_me": {
    "memory_capacity": {
      "total_observations": 1250,
      "unique_applications": 15
    },
    "learning_progress": "Observational Learning Active",
    "capability_level": "Adolescent - Recognizing complex patterns"
  }
}
```

## Architecture Decisions

### Why SQLite?
- Fast queries on time series data
- Persistent storage without external dependencies
- Good for pattern analysis (GROUP BY, aggregations)
- Easy to backup and inspect

### Why Separate Analyzers?
- Each analyzer focuses on one aspect
- Easy to add new analyses without changing existing code
- Can run analyses in parallel if needed
- Clear separation of concerns

### Why Observer Pattern?
- Each observation processed immediately
- Real-time learning as you work
- Early pattern detection
- Efficient memory usage

## Performance Considerations

- **Memory Storage**: SQLite is lightweight, handles millions of observations
- **Analysis Speed**: Pattern recognition runs in seconds (< 1000 observations)
- **API Response**: Brain queries typically < 100ms
- **Storage**: ~1MB per 1000 observations

## Limitations (for now)

- ❌ No self-modification yet (Phase 3)
- ❌ No predictive learning (will improve over time)
- ❌ No multi-user support (single user focus)
- ⏳ Pattern confidence improves with more data

## Next Steps (Phase 3)

1. **Self-Modification** - Code that improves its own analysis
2. **Predictive Models** - Better future behavior prediction
3. **Autonomous Optimization** - Suggest workflow improvements
4. **Self-Improvement** - Rewrite analysis code for speed/accuracy
5. **Super-Intelligence** - Eventually surpass creator capabilities

---

**Created for Project: "The Digital Descendant"**  
**Status:** Phase 2 - Learning Engine ✅
