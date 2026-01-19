import subprocess
import os
import sys

class Runner:
    def __init__(self):
        pass

    def run_code(self, script_path):
        """Runs the given script and returns the output"""
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout
            if result.stderr:
                output += "\nErrors:\n" + result.stderr
            return output
        except Exception as e:
            return f"Error running code: {e}"

    def execute_task(self, script_path):
        """Execute a task script"""
        return self.run_code(script_path)
