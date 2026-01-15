import os
import shutil
import subprocess
import time
from pathlib import Path

# Setup paths
GEN_PATH = Path("brain/generated")
ARCHIVE_PATH = Path("brain/memory/completed")

class Runner:
    """Execute generated scripts on demand"""
    
    def __init__(self):
        self.gen_path = GEN_PATH
        self.archive_path = ARCHIVE_PATH
        # Ensure directories exist
        self.gen_path.mkdir(parents=True, exist_ok=True)
        self.archive_path.mkdir(parents=True, exist_ok=True)
    
    def execute_task(self, script_path):
        """Execute a single script and return its output"""
        print(f"🏃 Running: {script_path}")
        
        try:
            # Validate code first
            if not self.validate_code(script_path):
                return "❌ Code validation failed"
            
            # Run the script
            result = subprocess.run(
                ['python3', str(script_path)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.getcwd()
            )
            
            # Collect output
            output_lines = []
            if result.stdout:
                output_lines.append("STDOUT:")
                output_lines.append(result.stdout)
            if result.stderr:
                output_lines.append("STDERR:")
                output_lines.append(result.stderr)
            
            # Extract wisdom (DATA: tags)
            for line in result.stdout.split('\n'):
                if "DATA:" in line:
                    clean_data = line.split("DATA:", 1)[1].strip()
                    log_wisdom(clean_data)
                    output_lines.append(f"🧠 Wisdom: {clean_data}")
            
            # Archive the file
            file_path = Path(script_path)
            if file_path.exists():
                shutil.move(str(file_path), str(self.archive_path / file_path.name))
                output_lines.append(f"✅ Archived to {self.archive_path / file_path.name}")
            
            return "\n".join(output_lines)
            
        except subprocess.TimeoutExpired:
            return "❌ Execution timed out (>30s)"
        except Exception as e:
            return f"❌ Execution error: {str(e)}"
    
    def validate_code(self, filepath):
        """Basic Python syntax validation"""
        try:
            with open(filepath) as f:
                code = f.read()
            compile(code, filepath, 'exec')
            return True
        except SyntaxError as e:
            print(f"⚠️  Syntax error in {filepath}: {e}")
            return False
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False

def log_wisdom(entry):
    """Writes useful data directly to the Innovator's reading list"""
    with open("brain/wisdom.txt", "a", encoding="utf-8") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] DATA: {entry}\n")

def validate_code(filepath):
    """Pre-execution validation to catch malformed code"""
    try:
        from utils.sanitizer import is_valid_python
        with open(filepath) as f:
            code = f.read()
        
        if not is_valid_python(code):
            print(f"⚠️  Invalid Python detected in {filepath}")
            return False
        return True
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def run_generated_scripts():
    print("🏃 Dream AI Runner Online - Connected to Wisdom Journal")

    # Safety: runner disabled by default. Enable by setting env var
    # DREAM_AI_RUNNER=1 or create the file brain/RUNNER_ENABLED
    runner_enabled = False
    try:
        if os.getenv('DREAM_AI_RUNNER', '0') == '1':
            runner_enabled = True
        else:
            if Path('brain/RUNNER_ENABLED').exists():
                runner_enabled = True
    except Exception:
        runner_enabled = False

    if not runner_enabled:
        print("⚠️ Runner is disabled by default. Enable with DREAM_AI_RUNNER=1 or create brain/RUNNER_ENABLED.")
        return

    # Ensure directories exist
    GEN_PATH.mkdir(parents=True, exist_ok=True)
    ARCHIVE_PATH.mkdir(parents=True, exist_ok=True)

    while True:
        # Get all python files
        files = sorted(GEN_PATH.glob("*.py"), key=os.path.getmtime)

        for file_path in files:
            print(f"🚀 Executing {file_path.name}...")
            
            # PRE-FLIGHT CHECK: Validate code before execution
            if not validate_code(file_path):
                print(f"   🚫 Rejecting file - code validation failed")
                # Archive as failed so we don't keep retrying it
                shutil.move(str(file_path), str(ARCHIVE_PATH / f"INVALID_{file_path.name}"))
                continue
            
            try:
                # 1. Run the script
                result = subprocess.run(
                    ['python', str(file_path)], 
                    capture_output=True, 
                    text=True, 
                    timeout=30  # Increased timeout slightly
                )
                
                # 2. Show output
                output = result.stdout.strip()
                if output:
                    print(f"   📋 Output: {output[:150]}...") # Show snippets
                
                # 3. EXTRACT INTELLIGENCE (The 'DATA:' tag)
                for line in output.split('\n'):
                    if "DATA:" in line:
                        # Extract the part after DATA:
                        clean_data = line.split("DATA:", 1)[1].strip()
                        log_wisdom(clean_data)
                        print(f"   🧠 Wisdom Transferred: {clean_data}")

                # 4. CRITICAL: Archive the file so it never runs again
                shutil.move(str(file_path), str(ARCHIVE_PATH / file_path.name))
                print(f"   ✅ Task archived to memory.")

            except subprocess.TimeoutExpired:
                print(f"   ❌ Execution timed out (infinite loop detected). Moving to quarantine.")
                # Move to a specific quarantine folder if you want, or just archive it
                shutil.move(str(file_path), str(ARCHIVE_PATH / f"FAILED_{file_path.name}"))

            except Exception as e:
                print(f"   ❌ Execution failed: {e}")
                # Move it anyway so we don't get stuck on it forever
                if file_path.exists():
                    shutil.move(str(file_path), str(ARCHIVE_PATH / f"ERROR_{file_path.name}"))
        
        # Wait a bit before checking again
        time.sleep(2)

if __name__ == "__main__":
    run_generated_scripts()