import os
import random
import re  # Added regex for parsing numbers

from .llm_client import LLMClient

# Optional web researcher for internet-assisted tasks
try:
    from brain.utils.web_researcher import WebResearcher
except Exception:
    WebResearcher = None

class Developer:
    def __init__(self):
        self.gen_path = "brain/generated"
        if not os.path.exists(self.gen_path):
            os.makedirs(self.gen_path)
        self.llm = LLMClient()

    def generate_solution(self, task):
        print(f"🛠️  Developer: Synthesizing INTELLIGENT code for -> {task}")
        task_raw = task
        task = task.lower()
        
        # Use LLM when available for open-ended coding tasks
        use_llm = self.llm.is_configured() and (
            "write" in task or "code" in task or "generate" in task or "script" in task or "llm" in task
            or os.getenv("LLM_ALWAYS", "0") == "1"
        )
        
        # Fast path for LLM-backed generation
        if use_llm:
            return self._generate_via_llm(task)
        
        # 1. SETUP & IMPORTS
        imports = ["import os", "import shutil", "import datetime", "import math"]
        header = []
        body = []
        footer = []

        # --- SKILL 1: MATH & LOGIC (NEW!) ---
        # This allows the AI to parse "Calculate 5 * 10" and write code for it
        if "calculate" in task or "math" in task or "solve" in task:
            header.append("def solve_math():")
            body.append("    print('🧮 AI Mathematician Starting...')")
            
            # Extract numbers from the task using Regex
            numbers = re.findall(r'\d+', task)
            if len(numbers) >= 2:
                op_symbol = "*" if "multiply" in task or "*" in task else "+"
                op_symbol = "/" if "divide" in task or "/" in task else op_symbol
                op_symbol = "-" if "subtract" in task or "-" in task else op_symbol
                
                # The AI writes the logic into the generated script
                body.append(f"    a = {numbers[0]}")
                body.append(f"    b = {numbers[1]}")
                body.append(f"    result = a {op_symbol} b")
                body.append(f"    print(f'✅ Calculation: {{a}} {op_symbol} {{b}} = {{result}}')")
                body.append("    print(f'DATA: Math result is {{result}}')")
            else:
                body.append("    print('❌ Error: I need two numbers to calculate.')")
            
            footer.append("if __name__ == '__main__':\n    solve_math()")

        # --- SKILL 2: DASHBOARD (Refined) ---
        elif "html" in task or "dashboard" in task:
            header.append("def create_dashboard():")
            body.append("    filename = 'dashboard.html'")
            body.append("    print(f'🎨 Creating Dashboard: {filename}...')")
            body.append("    # Dynamic Content")
            body.append("    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')")
            body.append("    html = f\"\"\"")
            body.append("<html><body style='background:#111;color:#0f0;font-family:monospace;padding:50px;'>")
            body.append("<h1>✨ DREAM AI STATUS ✨</h1>")
            body.append(f"<p>Generated at: {timestamp}</p>")
            body.append("<p>System: ONLINE</p>")
            body.append("<p>Intelligence Level: PHASE 3 (LOGIC)</p>")
            body.append("</body></html>\"\"\"")
            body.append("    try:")
            body.append("        with open(filename, 'w') as f: f.write(html)")
            body.append("        print(f'✅ SUCCESS: {filename} created!')")
            body.append("    except Exception as e:")
            body.append("        print(f'❌ Error: {e}')")
            footer.append("if __name__ == '__main__':\n    create_dashboard()")

        # --- SKILL 3b: CRYPTO PRICE (CoinGecko) ---
        elif ("bitcoin" in task or "ethereum" in task or "crypto" in task or "coingecko" in task) and ("price" in task or "quote" in task):
            imports.extend(["import requests", "import sys", "import json"]) 
            header.append("def fetch_price(coin: str = 'bitcoin', vs: str = 'usd'):")
            body.append("    url = 'https://api.coingecko.com/api/v3/simple/price'")
            body.append("    params = {'ids': coin, 'vs_currencies': vs}")
            body.append("    try:")
            body.append("        r = requests.get(url, params=params, timeout=10)")
            body.append("        r.raise_for_status()")
            body.append("        data = r.json()")
            body.append("        price = data.get(coin, {}).get(vs)")
            body.append("        if price is None:")
            body.append("            print('❌ Could not find price in response')")
            body.append("            return")
            body.append("        print(f'💱 {coin.capitalize()} price ({vs.upper()}): {price}')")
            body.append("        print(f'DATA: {coin}_{vs}={price}')")
            body.append("    except Exception as e:")
            body.append("        print(f'❌ Error fetching price: {e}')")
            body.append("")
            body.append("if __name__ == '__main__':")
            body.append("    coin = 'bitcoin'")
            body.append("    vs = 'usd'")
            body.append("    if len(sys.argv) > 1: coin = sys.argv[1]")
            body.append("    if len(sys.argv) > 2: vs = sys.argv[2]")
            body.append("    fetch_price(coin, vs)")
            # footer not needed since we added main guard

        # --- SKILL 4: SYSTEM PROCESSES (no extra deps) ---
        elif "check system processes" in task or ("process" in task and "check" in task):
            imports.extend(["import subprocess"])
            header.append("def top_processes(n: int = 5):")
            body.append("    try:")
            body.append("        cmd = 'ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n ' + str(n+1)")
            body.append("        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)")
            body.append("        print(res.stdout.strip())")
            body.append("        lines = [ln for ln in res.stdout.strip().split('\n') if ln][:n+1]")
            body.append("        if len(lines) > 1:")
            body.append("            print(f'DATA: top_process={lines[1]}')")
            body.append("    except Exception as e:")
            body.append("        print(f'❌ Error: {e}')")
            footer.append("if __name__ == '__main__':\n    top_processes(5)")

        # --- SKILL 5: WEB SEARCH (DuckDuckGo) ---
        elif "google" in task or "search" in task or "web" in task or "internet" in task or "bing" in task or "duckduckgo" in task or "research" in task:
            # Use WebResearcher if available; otherwise scaffold instructive placeholder
            if WebResearcher is not None:
                imports.extend(["import json"])
                header.append("def web_search(query: str):")
                body.append("    from brain.utils.web_researcher import WebResearcher")
                body.append("    wr = WebResearcher()")
                body.append("    results = wr.search_duckduckgo(query, max_results=5)")
                body.append("    if not results:")
                body.append("        print('❌ No results (or BeautifulSoup not installed). Install beautifulsoup4 to enable parsing).')")
                body.append("        return")
                body.append("    for i, r in enumerate(results, 1):")
                body.append("        print(f'{i}. {r.get(\"title\",\"\")}')")
                body.append("        print(f'   {r.get(\"url\",\"\")}')")
                body.append("        print(f'   {r.get(\"snippet\",\"\")}')")
                body.append("    print(f'DATA: top_url={results[0].get(\"url\",\"\")}')")
                body.append("")
                footer.append("if __name__ == '__main__':\n    web_search(\"" + task_raw.replace("\"","\\\"") + "\")")
            else:
                header.append("def web_search_placeholder():")
                body.append("    print('🔎 Web search requested but BeautifulSoup not installed.')")
                body.append("    print('Run: pip install beautifulsoup4')")
                body.append("    print('Then retry. Using DuckDuckGo HTML endpoint.')")
                footer.append("if __name__ == '__main__':\n    web_search_placeholder()")

        # --- SKILL 3: BACKUP (DEDUPLICATED) ---
        elif "backup" in task:
            imports.append("import time")
            header.append("def backup_system():")
            body.append("    source = 'brain'")
            body.append("    backups_dir = 'backups'")
            body.append("    if not os.path.exists(backups_dir): os.makedirs(backups_dir)")
            body.append("    ")
            body.append("    # Skip if backup was made in last hour")
            body.append("    recent_backup = None")
            body.append("    for d in os.listdir(backups_dir):")
            body.append("        path = os.path.join(backups_dir, d)")
            body.append("        if os.path.isdir(path):")
            body.append("            if time.time() - os.path.getmtime(path) < 3600:")
            body.append("                recent_backup = path")
            body.append("                break")
            body.append("    if recent_backup:")
            body.append("        print(f'⏭️  Backup skipped (recent backup exists)')")
            body.append("        return")
            body.append("    ")
            body.append("    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')")
            body.append("    dest = f'backups/brain_backup_{ts}'")
            body.append("    print(f'🚀 Starting Backup: {source} -> {dest}')")
            body.append("    try:")
            body.append("        shutil.copytree(source, dest, dirs_exist_ok=True)")
            body.append("        print('✅ Backup Complete.')")
            body.append("    except Exception as e:")
            body.append("        print(f'❌ Backup Failed: {e}')")
            footer.append("if __name__ == '__main__':\n    backup_system()")

        # --- FALLBACK ---
        else:
            if self.llm.is_configured():
                return self._generate_via_llm(task)
            # Generic HTTP JSON fetcher if an API is mentioned
            if "api" in task or "http" in task or "https" in task:
                imports.extend(["import requests", "import sys", "import json"])
                header.append("def fetch(url: str):")
                body.append("    try:")
                body.append("        r = requests.get(url, timeout=10)")
                body.append("        r.raise_for_status()")
                body.append("        ctype = r.headers.get('Content-Type','')")
                body.append("        if 'application/json' in ctype:")
                body.append("            print(json.dumps(r.json(), indent=2)[:2000])")
                body.append("        else:")
                body.append("            print(r.text[:2000])")
                body.append("        print(f'DATA: fetched_from={url}')")
                body.append("    except Exception as e:")
                body.append("        print(f'❌ Error: {e}')")
                footer.append("if __name__ == '__main__':\n    url = sys.argv[1] if len(sys.argv)>1 else 'https://httpbin.org/get'\n    fetch(url)")
            else:
                header.append("def check_status():")
                body.append("    print('✅ System Active - Waiting for specific command.')")
                footer.append("if __name__ == '__main__':\n    check_status()")

        # ASSEMBLE
        full_code = "\n".join(imports) + "\n\n" + "\n".join(header) + "\n" + "\n".join(body) + "\n\n" + "\n".join(footer)
        
        task_id = random.randint(10000, 99999)
        filename = f"{self.gen_path}/task_smart_{task_id}.py"
        with open(filename, "w") as f: f.write(full_code)
            
        return filename

    def _generate_via_llm(self, task: str) -> str:
        """Delegate code generation to the configured LLM."""
        system_prompt = (
            "You are a senior Python engineer. Write a complete, runnable Python script. "
            "Do not include explanations or markdown—only Python code. Use standard library unless specified."
        )
        user_prompt = f"Task: {task}\nReturn only Python code for a single file script."
        code = self.llm.generate_code(user_prompt, system_prompt, max_tokens=900)
        task_id = random.randint(10000, 99999)
        filename = f"{self.gen_path}/task_llm_{task_id}.py"
        with open(filename, "w") as f:
            f.write(code)
        return filename