# 🧪 HOW TO TEST YOUR DREAM AI

## Quick Tests (Use These!)

### 1️⃣ **Check If AI Is Running**
```bash
ps aux | grep -E "bridge.py|coordinator.py" | grep -v grep
```
**Expected:** 2 processes running (brain & eyes)

### 2️⃣ **Run Full Test Suite**
```bash
bash test_dream_ai.sh
```
**Expected:** All 5 tests pass ✅

### 3️⃣ **Test Brain Learning (Python)**
```python
from brain.orchestrator import BrainOrchestrator

brain = BrainOrchestrator()
insights = brain.analyze_patterns()
print(insights)
```
**Expected:** Insights about your work patterns

### 4️⃣ **Check Memory Storage**
```bash
ls -lh brain/memory/observations.db
ls brain/memory/completed/ | wc -l
```
**Expected:** Database file exists + 71 tasks listed

### 5️⃣ **Test Evolution System**
```bash
ls brain/evolution/*.py | wc -l
```
**Expected:** 21 evolution modules

---

## Interactive Tests

### Test A: Verify Brain Insights
```bash
cd /home/dheena/My_Life_Work/03_The_Dream_AI
python3 << 'EOF'
from brain.orchestrator import BrainOrchestrator

brain = BrainOrchestrator()
insights = brain.analyze_patterns()

print("\n📊 BRAIN INSIGHTS:")
for insight in insights.get('insights', [])[:5]:
    print(f"  • {insight.get('insight')}")
EOF
```

### Test B: Verify Skills Are Learned
```bash
python3 << 'EOF'
import json

with open("brain/memory/skills.json") as f:
    skills = json.load(f)

print(f"\n🎯 Learned Skills: {len(skills.get('skills', []))}")
for skill in skills.get('skills', [])[:5]:
    print(f"  • {skill.get('name', 'Unknown')}")
EOF
```

### Test C: Check Activities Being Tracked
```bash
python3 << 'EOF'
from brain.observation_memory import ObservationMemory

memory = ObservationMemory()
recent = memory.get_recent_observations(limit=5)

print(f"\n👁️ Recent Observations: {len(recent)}")
for obs in recent[:3]:
    print(f"  • {obs}")
EOF
```

---

## What Each Component Does

| Component | Test Command | What to Look For |
|-----------|--------------|-----------------|
| **Brain** | `ps aux \| grep bridge.py` | Should show running process |
| **Eyes** | `ps aux \| grep coordinator.py` | Should show running process |
| **Memory** | `ls -lh brain/memory/observations.db` | Should exist and have size |
| **Learning** | `ls brain/memory/completed/` | Should show 71+ task files |
| **Evolution** | `ls brain/evolution/*.py` | Should show 21+ modules |
| **Skills** | `cat brain/memory/skills.json` | Should list learned skills |

---

## Automated Test Results

Run this anytime to see full status:

```bash
cd /home/dheena/My_Life_Work/03_The_Dream_AI

# Full diagnostic
python3 test_ai.py

# Quick check
bash test_dream_ai.sh
```

---

## Expected Test Output

✅ **All tests pass if you see:**
- ✓ Brain running (PID shown)
- ✓ Eyes running (PID shown)  
- ✓ Database file exists
- ✓ 71+ completed tasks
- ✓ 21+ evolution modules
- ✓ Skills.json present

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Processes not running | Run: `bash start_dream_ai.sh` |
| Database empty | Normal after restart - will populate as AI observes |
| No skills listed | AI will learn them as it processes tasks |
| Tests timing out | Brain might be busy learning - wait 10 seconds |

---

## Advanced Testing

Monitor brain in real-time:
```bash
tail -f brain/brain.log
```

Check eyes observations:
```bash
tail -f brain/logs/*
```

---

**🎯 Your AI is ready to test!** Run `bash test_dream_ai.sh` right now to verify everything. ✅
