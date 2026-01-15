import os
import random
import re
import datetime
import subprocess
import json
from pathlib import Path

try:
    from googlesearch import search
except ImportError:
    search = None

try:
    from brain.evolution.ai_teacher import AITeacher
except ImportError:
    AITeacher = None

class SmartDeveloper:
    """
    SmartDeveloper - Generates Python code for various tasks
    
    Skills:
    🔍 Search - Google searches
    🧮 Math - Calculations
    📁 File Scanning - Find large files
    📋 Directory - List & analyze
    💾 Storage - Disk usage analysis
    📊 Reports - Generate summaries
    ✍️ Create - File creation
    🖥️ System - System info
    👁️ Monitor - Activity monitoring
    """
    
    def __init__(self):
        self.gen_path = "brain/generated"
        if not os.path.exists(self.gen_path):
            os.makedirs(self.gen_path)

    def generate_solution(self, task):
        print(f"🧠 Smart Developer: Analyzing request -> '{task}'")
        task_lower = task.lower()
        
        header = ["import os", "import json", "import datetime", "import sys", "from pathlib import Path"]
        body = []
        footer = ["if __name__ == '__main__':", "    run_task()"]
        
        task_id = random.randint(10000, 99999)
        filename = f"{self.gen_path}/task_smart_{task_id}.py"

        # SKILL ROUTING - Improved pattern matching
        # Check for most specific patterns FIRST
        
        # System monitoring (BEFORE web research to avoid "check" keyword match)
        if any(x in task_lower for x in ["process", "ps", "running", "service", "daemon", "system process"]):
            print("⚙️ Skill: Process Monitoring")
            body = self._skill_check_processes(task, header)
        elif any(x in task_lower for x in ["backup", "copy", "archive"]):
            print("💾 Skill: Backup")
            body = self._skill_backup(task, header)
        # File operations (before disk to be more specific)
        elif any(x in task_lower for x in ["scan", "large files", "find files"]):
            print("📁 Skill: File Scanning")
            body = self._skill_scan(task, header)
        elif "list" in task_lower and "file" in task_lower:
            print("📋 Skill: List Files")
            body = self._skill_list_files(task, header)
        # System monitoring - disk specific
        elif any(x in task_lower for x in ["disk space", "storage", "disk usage", "disk"]):
            print("💾 Skill: Disk Analysis")
            body = self._skill_disk_space(task, header)
        # Analyze directory (before general analyze)
        elif "analyze" in task_lower and "dir" in task_lower:
            print("📊 Skill: Directory Analysis")
            body = self._skill_analyze_dir(task, header)
        # Math and computation
        elif any(x in task_lower for x in ["calculate", "math", "+", "-", "*", "/", "multiplied", "divided"]):
            print("🧮 Skill: Math")
            body = self._skill_math(task, header)
        # File creation
        elif any(x in task_lower for x in ["create file", "write file", "make file"]):
            print("✍️ Skill: File Creation")
            body = self._skill_create_file(task, header)
        # System info
        elif any(x in task_lower for x in ["system", "status", "info", "whoami", "hostname", "uptime"]):
            print("🖥️ Skill: System Info")
            body = self._skill_system_info(task, header)
        # Python code examples
        elif any(x in task_lower for x in ["python code", "python", "script", "tutorial", "example", "code to work"]):
            print("🐍 Skill: Python Examples")
            body = self._skill_python_code(task, header)
        # Web Research Skills
        elif any(x in task_lower for x in ["bitcoin", "price", "weather", "stock", "crypto", "search", "google", "look up", "find info", "check", "what is", "who is", "where is", "news", "latest", "research", "learn about"]):
            print("🌐 Skill: Web Research")
            body = self._skill_web_research(task, header)
        # Games
        elif "game" in task_lower:
            print("🎮 Skill: Game Creation")
            body = self._skill_game(task, header)
        # GUI/Window
        elif any(x in task_lower for x in ["gui", "window", "interface", "app"]):
            print("🖥️ Skill: GUI Creation")
            body = self._skill_gui(task, header)
        # Fallback
        else:
            print("❓ Skill: Fallback")
            body = self._skill_fallback(task, header)

        # ASSEMBLE CODE
        full_code = "\n".join(header) + "\n\n" + "\n".join(body) + "\n\n" + "\n".join(footer)
        
        with open(filename, "w") as f:
            f.write(full_code)
            
        return filename

    # ============ SKILLS ============

    def _skill_web_research(self, task, header):
        """Web Research - Bitcoin, Weather, Stock prices, etc."""
        header.append("import urllib.request")
        header.append("import urllib.parse")
        
        # Extract query from task
        query = task.replace("find", "").replace("check", "").replace("what is", "").replace("search for", "").strip()
        
        body = [
            "def run_task():",
            f"    query = '{query}'",
            "    print(f'🌐 Web Research: {query}...')",
            "    try:",
        ]

        if "bitcoin" in query.lower() or "price" in query.lower() or "crypto" in query.lower():
            body.extend([
                "        print('  💰 Checking Bitcoin/Price data...')",
                "        import json",
                "        url = 'https://api.coinbase.com/v2/prices/BTC-USD/spot'",
                "        try:",
                "            req = urllib.request.Request(url)",
                "            with urllib.request.urlopen(req, timeout=5) as response:",
                "                data = json.loads(response.read().decode())",
                "                price = data.get('data', {}).get('amount', 'N/A')",
                "                print(f'  💹 Bitcoin Price (USD): ${price}')",
                "        except Exception as e:",
                "            print(f'  ℹ️  Bitcoin API unavailable: {e}')",
            ])

        elif "weather" in query.lower():
            body.extend([
                "        print('  ☁️  Checking Weather data...')",
                "        try:",
                "            url = 'https://wttr.in?format=3'",
                "            req = urllib.request.Request(url)",
                "            with urllib.request.urlopen(req, timeout=5) as response:",
                "                weather = response.read().decode().strip()",
                "                print(f'  🌡️  Weather: {weather}')",
                "        except Exception as e:",
                "            print(f'  ℹ️  Weather API unavailable: {e}')",
            ])

        else:
            body.extend([
                "        # General Search",
                "        print(f'  🔍 For detailed info, search: \"{query}\" on Google')",
                "        print(f'  💡 Recommended: Google.com, Wikipedia, etc.')",
            ])

        body.extend([
            "        print('✅ Web research query prepared')",
            "    except Exception as e:",
            "        print(f'❌ Web research error: {e}')",
        ])

        return body

    def _skill_game(self, task, header):
        """Create a simple game"""
        body = [
            "def run_task():",
            "    print('🎮 Starting Guess the Number Game...')",
            "    target = 42",  # Fixed for automation, normally random
            "    print('  I am thinking of a number between 1 and 100.')",
            "    # Simulating a game loop for automation",
            "    guesses = [10, 50, 42]",
            "    for guess in guesses:",
            "        print(f'  Player guesses: {guess}')",
            "        if guess < target:",
            "            print('  🤖 Higher!')",
            "        elif guess > target:",
            "            print('  🤖 Lower!')",
            "        else:",
            "            print('  🎉 Correct! You win!')",
            "            break",
        ]
        return body

    def _skill_gui(self, task, header):
        """Create a simple GUI (Tkinter)"""
        header.append("import tkinter as tk")
        body = [
            "def run_task():",
            "    print('🖥️  Launching GUI Application...')",
            "    try:",
            "        root = tk.Tk()",
            "        root.title('Dream AI App')",
            "        label = tk.Label(root, text='Hello from Dream AI!', font=('Arial', 24))",
            "        label.pack(padx=20, pady=20)",
            "        print('  ✅ GUI Window created (close window to finish task)')",
            "        # Auto-close for automation testing",
            "        root.after(2000, root.destroy)",
            "        root.mainloop()",
            "        print('  ✅ GUI Closed')",
            "    except Exception as e:",
            "        print(f'❌ GUI Error (Headless environment?): {e}')",
        ]
        return body

    def _skill_scan(self, task, header):
        """Scan for large files"""
        body = [
            "def run_task():",
            "    target = 'brain'",
            "    size_mb = 5",
            "    print(f'🔍 Scanning {target} for files > {size_mb}MB...')",
            "    large_files = []",
            "    try:",
            "        for root, dirs, files in os.walk(target):",
            "            for file in files:",
            "                path = os.path.join(root, file)",
            "                try:",
            "                    size_mb = os.path.getsize(path) / (1024*1024)",
            "                    if size_mb > 5:",
            "                        large_files.append((file, size_mb))",
            "                        print(f'  📦 {file}: {size_mb:.2f}MB')",
            "                except:",
            "                    pass",
            "    except Exception as e:",
            "        print(f'❌ Error: {e}')",
            "    if not large_files:",
            "        print('✅ No large files found (all < 5MB)')",
            "    else:",
            "        print(f'✅ Found {len(large_files)} large files')",
        ]
        return body

    def _skill_list_files(self, task, header):
        """List files in directory"""
        body = [
            "def run_task():",
            "    path = 'brain'",
            "    print(f'📋 Listing files in: {path}')",
            "    try:",
            "        for item in sorted(os.listdir(path))[:20]:",
            "            full_path = os.path.join(path, item)",
            "            if os.path.isdir(full_path):",
            "                print(f'  📁 {item}/')",
            "            else:",
            "                try:",
            "                    size = os.path.getsize(full_path)",
            "                    print(f'  📄 {item} ({size} bytes)')",
            "                except:",
            "                    print(f'  📄 {item}')",
            "    except Exception as e:",
            "        print(f'❌ Error: {e}')",
        ]
        return body

    def _skill_disk_space(self, task, header):
        """Analyze disk usage"""
        body = [
            "def run_task():",
            "    import shutil",
            "    print('💾 Analyzing disk space...')",
            "    try:",
            "        total, used, free = shutil.disk_usage('/')",
            "        total_gb = total // (1024**3)",
            "        used_gb = used // (1024**3)",
            "        free_gb = free // (1024**3)",
            "        used_pct = 100 * used // total",
            "        print(f'  Total: {total_gb} GB')",
            "        print(f'  Used:  {used_gb} GB ({used_pct}%)')",
            "        print(f'  Free:  {free_gb} GB')",
            "        if free_gb < 10:",
            "            print('⚠️  Low disk space warning!')",
            "        else:",
            "            print('✅ Disk space is healthy')",
            "    except Exception as e:",
            "        print(f'❌ Error: {e}')",
        ]
        return body

    def _skill_analyze_dir(self, task, header):
        """Analyze directory structure"""
        body = [
            "def run_task():",
            "    target = 'brain'",
            "    print(f'📊 Analyzing: {target}')",
            "    file_count = 0",
            "    dir_count = 0",
            "    total_size = 0",
            "    try:",
            "        for root, dirs, files in os.walk(target):",
            "            dir_count += len(dirs)",
            "            for file in files:",
            "                file_count += 1",
            "                path = os.path.join(root, file)",
            "                try:",
            "                    total_size += os.path.getsize(path)",
            "                except:",
            "                    pass",
            "    except Exception as e:",
            "        print(f'❌ Error: {e}')",
            "    size_mb = total_size / (1024*1024)",
            "    print(f'  📁 Directories: {dir_count}')",
            "    print(f'  📄 Files: {file_count}')",
            "    print(f'  💾 Total Size: {size_mb:.2f} MB')",
        ]
        return body

    def _skill_math(self, task, header):
        """Math calculations"""
        numbers = re.findall(r'\d+\.?\d*', task)
        
        if len(numbers) >= 2:
            # Detect operator
            if any(x in task for x in ["*", "multiply", "multiplied", "times"]):
                op = "*"
            elif any(x in task for x in ["/", "divide", "divided"]):
                op = "/"
            elif any(x in task for x in ["-", "minus", "subtract"]):
                op = "-"
            else:
                op = "+"
            
            body = [
                "def run_task():",
                f"    a = {numbers[0]}",
                f"    b = {numbers[1]}",
                f"    print(f'🧮 Calculating {{a}} {op} {{b}}...')",
                f"    result = a {op} b",
                "    print(f'✅ Result: {result}')",
            ]
        else:
            body = [
                "def run_task():",
                "    print('❌ Error: Need at least 2 numbers')",
            ]
        return body

    def _skill_create_file(self, task, header):
        """Create a file"""
        filename = "notes.txt"
        words = task.split()
        if "named" in words:
            try:
                idx = words.index("named")
                filename = words[idx+1]
            except:
                pass
        
        body = [
            "def run_task():",
            f"    filename = '{filename}'",
            "    content = 'File created by Dream AI\\\\n'",
            "    content += f'Created: {datetime.datetime.now()}'",
            "    with open(filename, 'w') as f:",
            "        f.write(content)",
            "    print(f'✅ Created: {filename}')",
        ]
        return body
    
    def _skill_check_processes(self, task, header):
        """Check running processes"""
        header.append("import subprocess")
        body = [
            "def run_task():",
            "    print('⚙️ Checking System Processes...')",
            "    try:",
            "        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)",
            "        lines = result.stdout.strip().split('\\\\n')",
            "        print(f'Total processes: {len(lines) - 1}')",
            "        print('Top 5 by memory:')",
            "        for line in sorted(lines[1:], key=lambda x: float(x.split()[3]) if len(x.split()) > 3 else 0, reverse=True)[:5]:",
            "            cols = line.split()",
            "            if len(cols) > 10:",
            "                print(f'  {cols[10]}: {cols[3]}% MEM')",
            "    except Exception as e:",
            "        print(f'❌ Error: {e}')",
        ]
        return body
    
    def _skill_backup(self, task, header):
        """Backup brain folder"""
        header.append("import shutil")
        body = [
            "def run_task():",
            "    print('💾 Creating Backup...')",
            "    import datetime",
            "    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')",
            "    backup_name = f'backups/brain_backup_{timestamp}'",
            "    try:",
            "        shutil.copytree('brain', backup_name)",
            "        print(f'✅ Backup created: {backup_name}')",
            "    except Exception as e:",
            "        print(f'❌ Backup failed: {e}')",
        ]
        return body
    
    def _skill_python_code(self, task, header):
        """Generate Python code examples"""
        body = [
            "def run_task():",
            f"    print('🐍 Python Code Example')",
            f"    print('Task: {task}')",
            "    print('\\\\nExample code:')",
            "    print('# Working with files')",
            "    print('with open(\"example.txt\", \"w\") as f:')",
            "    print('    f.write(\"Hello World\")')",
            "    print('\\\\n# Reading files')",
            "    print('with open(\"example.txt\", \"r\") as f:')",
            "    print('    content = f.read()')",
            "    print('    print(content)')",
        ]
        return body

    def _skill_system_info(self, task, header):
        """System information"""
        header.append("import psutil")
        header.append("import platform")
        header.append("import time")
        header.append("import datetime")

        body = [
            "def run_task():",
            "    print('🖥️  ROBUST SYSTEM HEALTH CHECK')",
            "    print('='*40)",
            "",
            "    # 1. System Info",
            "    print('📌 SYSTEM:')",
            "    try:",
            "        print(f'  OS: {platform.system()} {platform.release()}')",
            "        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())",
            "        uptime = datetime.datetime.now() - boot_time",
            "        print(f'  Boot Time: {boot_time.strftime(\"%Y-%m-%d %H:%M:%S\")}')",
            "        print(f'  Uptime: {str(uptime).split(\".\")[0]}')",
            "    except Exception as e: print(f'  Error: {e}')",
            "",
            "    # 2. CPU Usage",
            "    print('\\n🧠 CPU:')",
            "    try:",
            "        print(f'  Physical Cores: {psutil.cpu_count(logical=False)}')",
            "        print(f'  Total Threads: {psutil.cpu_count(logical=True)}')",
            "        # Initial call returns 0, so we sleep briefly or accept the first read",
            "        cpu_pct = psutil.cpu_percent(interval=1)",
            "        print(f'  CPU Usage: {cpu_pct}%')",
            "        if hasattr(psutil, 'getloadavg'):",
            "            print(f'  Load Avg: {psutil.getloadavg()}')",
            "        elif hasattr(os, 'getloadavg'):",
            "            print(f'  Load Avg: {os.getloadavg()}')",
            "    except Exception as e: print(f'  Error: {e}')",
            "",
            "    # 3. Memory Usage",
            "    print('\\n💾 MEMORY:')",
            "    try:",
            "        mem = psutil.virtual_memory()",
            "        total_gb = mem.total / (1024**3)",
            "        avail_gb = mem.available / (1024**3)",
            "        print(f'  Total: {total_gb:.2f} GB')",
            "        print(f'  Available: {avail_gb:.2f} GB')",
            "        print(f'  Used: {mem.percent}%')",
            "    except Exception as e: print(f'  Error: {e}')",
            "",
            "    # 4. Disk Usage",
            "    print('\\n💿 DISK (Root):')",
            "    try:",
            "        disk = psutil.disk_usage('/')",
            "        total_d = disk.total / (1024**3)",
            "        used_d = disk.used / (1024**3)",
            "        free_d = disk.free / (1024**3)",
            "        print(f'  Total: {total_d:.2f} GB')",
            "        print(f'  Used: {used_d:.2f} GB ({disk.percent}%)')",
            "        print(f'  Free: {free_d:.2f} GB')",
            "    except Exception as e: print(f'  Error: {e}')",
            "",
            "    print('='*40)",
            "    print('✅ Health Check Complete')",
        ]
        return body

    def _skill_fallback(self, task, header):
        """Fallback for unknown tasks"""
        body = [
            "def run_task():",
            f"    print('🤖 I heard: {task}')",
            "    print('🧠 Learning mode: Analyzing patterns...')",
            "    print('💡 Skills available: search, math, scan, analyze, list files, disk space, system info')",
            "    print('⚠️  This task type not in my skillset yet, but I am learning!')",
        ]
        return body
