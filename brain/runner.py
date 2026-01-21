import subprocess
import os
import sys

class Runner:
    """
    Runner - Executes code and tasks.
    """
    def __init__(self):
        pass

    def run_code(self, code_path):
        """
        Runs a python script and returns the output.
        """
        return self.execute_task(code_path)

    def execute_task(self, script_path):
        """
        Executes the python script at script_path.
        """
        print(f"🏃 Runner: Executing {script_path}...")
        try:
            # Check if file exists
            if not os.path.exists(script_path):
                return f"❌ Error: File not found: {script_path}"

            # Execute
            process = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=60
            )

            output = ""
            if process.stdout:
                output += process.stdout
            if process.stderr:
                output += f"\n❌ Errors:\n{process.stderr}"

            return output

        except subprocess.TimeoutExpired:
            return "❌ Error: Execution timed out (60s limit)"
        except Exception as e:
            return f"❌ Runner Error: {e}"
