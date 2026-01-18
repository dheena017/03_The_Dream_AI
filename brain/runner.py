"""
RUNNER - The Hand of the AI
Executes generated code and skills
"""

import subprocess
import sys
import os

class Runner:
    """Executes Python code and scripts"""

    def __init__(self):
        pass

    def execute_task(self, script_path):
        """Execute a Python script file"""
        return self._run_script(script_path)

    def run_code(self, script_path):
        """Run code (alias for execute_task since we pass paths)"""
        return self._run_script(script_path)

    def _run_script(self, script_path):
        """Internal method to run script"""
        if not os.path.exists(script_path):
            return f"❌ Error: File not found: {script_path}"

        try:
            # Run with same python executable
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=60  # Prevent infinite loops
            )

            output = ""
            if result.stdout:
                output += f"{result.stdout}\n"
            if result.stderr:
                output += f"⚠️ STDERR:\n{result.stderr}\n"

            if result.returncode != 0:
                output += f"\n❌ Process exited with code {result.returncode}"

            return output

        except subprocess.TimeoutExpired:
            return "❌ Error: Execution timed out (60s limit)"
        except Exception as e:
            return f"❌ Execution Error: {e}"
