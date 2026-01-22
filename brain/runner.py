import subprocess
import sys
import os

class Runner:
    """Executes code and tasks"""

    def __init__(self):
        pass

    def execute_task(self, script_path):
        """Execute a python script"""
        if not os.path.exists(script_path):
            return f"❌ Error: File not found: {script_path}"

        try:
            # Run with same python interpreter
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            output = result.stdout
            if result.stderr:
                output += "\nErrors:\n" + result.stderr
            return output
        except Exception as e:
            return f"❌ Execution failed: {e}"

    def run_code(self, script_path):
        """Run code (alias for execute_task for now)"""
        return self.execute_task(script_path)
