import os
import re
import urllib.request
import urllib.parse
import json

class Innovator:
    def __init__(self, mode="sysadmin"):
        self.wisdom_path = "brain/wisdom.txt"
        self.inbox_path = "brain/tasks.txt"
        self.recent_tasks = []  # Memory of recent tasks
        self.max_memory = 5     # Remember last 5 tasks
        
        # 🎯 PRIME DIRECTIVE: The AI's purpose/focus
        self.mode = mode
        print(f"🎯 PRIME DIRECTIVE: {mode.upper()} MODE")
        
        # Define mode-specific task pools
        self.mode_tasks = {
            "sysadmin": [
                "AUTONOMOUS_TASK: scan for large files in brain folder",
                "AUTONOMOUS_TASK: check system processes",
                "AUTONOMOUS_TASK: analyze disk usage",
                "AUTONOMOUS_TASK: review system health",
            ],
            "python_learner": [
                "AUTONOMOUS_TASK: Find python code to implement Fibonacci sequence",
                "AUTONOMOUS_TASK: Find python code to sort a list",
                "AUTONOMOUS_TASK: Find python code to parse JSON",
                "AUTONOMOUS_TASK: Find python code to work with files",
            ],
            "researcher": [
                "AUTONOMOUS_TASK: search for latest AI news",
                "AUTONOMOUS_TASK: search for python best practices",
                "AUTONOMOUS_TASK: search for machine learning tutorials",
                "AUTONOMOUS_TASK: search for coding algorithms",
            ]
        }

    def run_autonomy(self):
        print("💤 INNOVATOR: Reading Wisdom...")
        
        try:
            # 1. Read Wisdom
            last_data = ""
            if os.path.exists(self.wisdom_path):
                with open(self.wisdom_path, "r") as f:
                    lines = f.readlines()
                    if lines: last_data = lines[-1].strip()

            print(f"📖 Insight: {last_data}")

            # 2. DECISION MATRIX - Mode-Aware Task Selection
            # Get tasks for current mode
            available_tasks = self.mode_tasks.get(self.mode, self.mode_tasks["sysadmin"])
            
            print(f"🎯 Mode: {self.mode.upper()} | Task Pool: {len(available_tasks)} options")
            
            # Filter out recently done tasks (boredom logic)
            fresh_tasks = [t for t in available_tasks if t not in self.recent_tasks]
            
            # If all tasks were done recently, reset memory
            if not fresh_tasks:
                self.recent_tasks = []
                fresh_tasks = available_tasks
            
            next_task = fresh_tasks[0]  # Default to first fresh task

            if "Found" in last_data and "large files" in last_data:
                count = 0
                match = re.search(r'Found (\d+)', last_data)
                if match: count = int(match.group(1))

                if count > 0:
                    print(f"💡 INNOVATOR: {count} large files found. DECISION -> Backup immediately.")
                    next_task = "AUTONOMOUS_TASK: backup the brain folder"
                else:
                    print("💡 INNOVATOR: No large files. DECISION -> Check System Health.")
                    next_task = "AUTONOMOUS_TASK: check system processes"

            elif "Backup created" in last_data:
                 print("💡 INNOVATOR: Backup safe. DECISION -> Relax and Monitor.")
                 next_task = "AUTONOMOUS_TASK: check system processes"

            self._post_task(next_task)

        except Exception as e:
            print(f"⚠️ Innovator Error: {e}")
            self._post_task("AUTONOMOUS_TASK: scan for large files")

    def _post_task(self, task):
        # Add to memory to prevent repetition
        self.recent_tasks.append(task)
        if len(self.recent_tasks) > self.max_memory:
            self.recent_tasks.pop(0)  # Remove oldest
        
        print(f"✨ INNOVATOR: Posted task: {task}")
        print(f"🧠 Task Memory: {len(self.recent_tasks)} tasks remembered")
        
        # 🔗 PHASE 7: Call Bridge directly via HTTP
        self._execute_task_via_bridge(task)
    
    def _execute_task_via_bridge(self, task):
        """Send task directly to Bridge via HTTP (closes the circuit)"""
        try:
            url = "http://localhost:3000/command"
            data = json.dumps({"task": task}).encode('utf-8')
            
            req = urllib.request.Request(
                url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode())
                print(f"📞 Bridge responded: {result.get('status', {}).get('status', 'unknown')}")
                
        except Exception as e:
            print(f"⚠️  Could not reach Bridge: {e}")
            print(f"💾 Falling back to file-based task queue...")
            with open(self.inbox_path, "w") as f:
                f.write(task)

# Module-level helper for the Bridge
def run_autonomy():
    agent = Innovator()
    agent.run_autonomy()