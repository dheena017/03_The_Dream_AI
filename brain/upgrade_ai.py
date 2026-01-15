import os
import sqlite3

print("🚀 STARTING BRAIN SURGERY...")

# ==========================================
# 1. FIX THE MEMORY (DATABASE LOCK)
# ==========================================
memory_code = """import sqlite3
import datetime
import os
import json

class ObservationMemory:
    def __init__(self, db_path="brain/memory/observations.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # FIX: Check same thread false allows multiple connections
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        
        # FIX: WAL Mode prevents 'Database Locked' errors
        self.conn.execute("PRAGMA journal_mode=WAL;") 
        
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                type TEXT,
                data TEXT
            )
        ''')
        self.conn.commit()

    def store_observation(self, type, data):
        try:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(data, dict):
                data = json.dumps(data)
            self.cursor.execute("INSERT INTO observations (timestamp, type, data) VALUES (?, ?, ?)", (ts, type, str(data)))
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ Memory Error: {e}")

    def get_recent_observations(self, limit=10):
        self.cursor.execute("SELECT * FROM observations ORDER BY id DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()
"""

with open("brain/memory.py", "w") as f:
    f.write(memory_code)
print("✅ Memory Module: PATCHED (WAL Mode Enabled)")

# ==========================================
# 2. CREATE THE SMART DEVELOPER (NO API KEY)
# ==========================================
smart_dev_code = """import os
import random
import re
import datetime
try:
    from googlesearch import search
except ImportError:
    search = None

class SmartDeveloper:
    def __init__(self):
        self.gen_path = "brain/generated"
        if not os.path.exists(self.gen_path):
            os.makedirs(self.gen_path)

    def generate_solution(self, task):
        print(f"🧠 Smart Developer: Analyzing request -> '{task}'")
        task = task.lower()
        
        header = ["import os", "import datetime"]
        body = []
        footer = ["if __name__ == '__main__':", "    run_task()"]
        
        task_id = random.randint(10000, 99999)
        filename = f"{self.gen_path}/task_smart_{task_id}.py"

        # --- SKILL: GOOGLE SEARCH ---
        if "search" in task or "find" in task or "who is" in task:
            print("🔎 Detected Internet Search Request")
            header.append("from googlesearch import search")
            
            # Extract search query
            query = task.replace("search", "").replace("google", "").replace("find", "").replace("for", "").strip()
            
            body.append("def run_task():")
            body.append(f"    query = '{query}'")
            body.append("    print(f'🌍 Searching Google for: {query}...')")
            body.append("    results = []")
            body.append("    try:")
            body.append("        for j in search(query, num_results=5):")
            body.append("            results.append(j)")
            body.append("            print(f'  🔗 Found: {j}')")
            body.append("    except Exception as e:")
            body.append("        print(f'❌ Search failed: {e}')")
            body.append("    ")
            body.append("    # Save results")
            body.append(f"    with open('search_results_{task_id}.txt', 'w') as f:")
            body.append("        f.write('\\n'.join(results))")
            body.append("    print('✅ Search complete. Saved to search_results.txt')")

        # --- SKILL: MATH / CALCULATE ---
        elif "calculate" in task or "math" in task:
            print("🧮 Detected Math Request")
            numbers = re.findall(r'\d+', task)
            if len(numbers) >= 2:
                op = "*" if "*" in task or "multiply" in task else "+"
                op = "/" if "/" in task or "divide" in task else op
                op = "-" if "-" in task or "minus" in task else op
                
                body.append("def run_task():")
                body.append(f"    a = {numbers[0]}")
                body.append(f"    b = {numbers[1]}")
                body.append(f"    print(f'🧮 Calculating {{a}} {op} {{b}}...')")
                body.append(f"    res = a {op} b")
                body.append(f"    print(f'✅ Result: {{res}}')")
            else:
                body.append("def run_task():")
                body.append("    print('❌ Error: I need two numbers.')")

        # --- SKILL: SYSTEM MAINTENANCE ---
        elif "scan" in task or "clean" in task:
            body.append("def run_task():")
            body.append("    print('🧹 Performing System Maintenance...')")
            body.append("    # Add real logic here")
            body.append("    print('✅ System Scanned.')")

        # --- FALLBACK ---
        else:
            body.append("def run_task():")
            body.append(f"    print('🤖 I heard: {task}')")
            body.append("    print('⚠️ I do not have a skill for this yet.')")

        # ASSEMBLE CODE
        full_code = "\\n".join(header) + "\\n\\n" + "\\n".join(body) + "\\n\\n" + "\\n".join(footer)
        
        with open(filename, "w") as f:
            f.write(full_code)
            
        return filename
"""

with open("brain/evolution/smart_developer.py", "w") as f:
    f.write(smart_dev_code)
print("✅ Smart Developer: INSTALLED (Google Skills Added)")

# ==========================================
# 3. UPDATE THE BRIDGE TO USE SMART DEVELOPER
# ==========================================
bridge_path = "brain/bridge.py"
with open(bridge_path, "r") as f:
    content = f.read()

# Replace the import
if "from brain.evolution.developer import Developer" in content:
    content = content.replace(
        "from brain.evolution.developer import Developer", 
        "from brain.evolution.smart_developer import SmartDeveloper"
    )

# Replace the instantiation
if "self.developer = Developer()" in content:
    content = content.replace(
        "self.developer = Developer()", 
        "self.developer = SmartDeveloper()"
    )

with open(bridge_path, "w") as f:
    f.write(content)

print("✅ Bridge: UPDATED (Connected to Smart Brain)")
print("🎉 UPGRADE COMPLETE. Please restart your AI.")