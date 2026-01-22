import subprocess
import os

class Runner:
    def __init__(self):
        pass

    def run_code(self, script_path):
        """Run a python script and return output"""
        try:
            if not os.path.exists(script_path):
                return f"❌ Error: File not found: {script_path}"

            result = subprocess.run(
                ['python3', script_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout + result.stderr
        except Exception as e:
            return f"❌ Execution Error: {e}"

    def execute_task(self, script_path):
        """Execute a task (alias for run_code for now)"""
        return self.run_code(script_path)
