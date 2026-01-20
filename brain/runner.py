"""
Runner - Code Execution Module
"""
import subprocess
import sys
import os

class Runner:
    def __init__(self):
        pass

    def run_code(self, code_path):
        """
        Executes code at code_path.
        """
        return self.execute_task(code_path)

    def execute_task(self, script_path):
        """
        Executes the script at script_path using subprocess.
        """
        try:
            print(f"🏃 Runner executing: {script_path}")
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout
            if result.stderr:
                output += "\nERROR:\n" + result.stderr
            return output
        except Exception as e:
            return f"❌ Execution Error: {str(e)}"
