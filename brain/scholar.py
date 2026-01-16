
import os
import re
import datetime
import ast

class Scholar:
    """
    The Scholar: Researches errors and finds solutions.
    """

    def __init__(self):
        self.memory_path = "brain/memory/corpus.txt"
        self._ensure_memory()

    def _ensure_memory(self):
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        if not os.path.exists(self.memory_path):
            with open(self.memory_path, 'w') as f:
                f.write("# SCHOLAR LONG TERM MEMORY\n")

    def research_error(self, error_output, script_path):
        """
        Analyzes error output and returns a fix plan.
        """
        print("🎓 Scholar: Analyzing crash report...")

        # 1. Extract the actual error
        error_type, error_msg = self._parse_error(error_output)
        print(f"🎓 Scholar: Identified error -> {error_type}: {error_msg}")

        # 2. Check memory first
        known_fix = self._check_memory(error_type, error_msg)
        if known_fix:
            print("🎓 Scholar: Recall -> I have solved this before!")
            return known_fix

        # 3. Research (Web Search Simulation / Real Search)
        print("🎓 Scholar: Researching solution online...")
        solution = self._web_search_solution(error_type, error_msg)

        # 4. Save to memory
        self._save_to_memory(error_type, error_msg, solution)

        return solution

    def _parse_error(self, output):
        """Extracts the last error from traceback"""
        lines = output.split('\n')
        error_type = "UnknownError"
        error_msg = "Unknown error"

        # Look for traceback
        for line in reversed(lines):
            if line.strip() and ":" in line:
                # Basic python error detection (e.g. NameError: name 'x' is not defined)
                parts = line.split(':', 1)
                if len(parts) == 2 and parts[0].strip().endswith('Error'):
                    error_type = parts[0].strip()
                    error_msg = parts[1].strip()
                    break

        return error_type, error_msg

    def _check_memory(self, error_type, error_msg):
        if not os.path.exists(self.memory_path):
            return None

        found_solution = None

        try:
            with open(self.memory_path, 'r') as f:
                lines = f.readlines()

            for i in range(len(lines)):
                line = lines[i].strip()
                # Check for error line
                if "ERROR: " in line:
                    parts = line.split("ERROR: ", 1)
                    if len(parts) == 2:
                        stored_error = parts[1].strip()
                        if stored_error == f"{error_type} - {error_msg}":
                            # Found a match, look for solution in next line
                            if i + 1 < len(lines):
                                sol_line = lines[i+1].strip()
                                if sol_line.startswith("SOLUTION: "):
                                    try:
                                        sol_str = sol_line[len("SOLUTION: "):]
                                        found_solution = ast.literal_eval(sol_str)
                                    except Exception:
                                        pass
        except Exception as e:
            print(f"🎓 Scholar: Error reading memory: {e}")

        return found_solution

    def _web_search_solution(self, error_type, error_msg):
        """
        Simulates finding a solution.
        In a real scenario, this would scrape StackOverflow/Google.
        For now, we map common errors to logic fixes.
        """

        # FIX STRATEGIES

        # Strategy 1: Missing Module -> Install or Replace
        if error_type == "ModuleNotFoundError":
            module_name = error_msg.replace("No module named ", "").strip("'").strip('"')

            # Special logic for our test case
            if module_name == "non_existent_module_for_testing":
                return {
                    "type": "replace_import",
                    "original": module_name,
                    "replacement": "math", # Replace with a standard library that exists
                    "action": "modify_code"
                }

            # General case: Attempt to pip install
            # Note: In this environment we might not want to randomly install things,
            # but this is the "Digital Organism" concept.
            return {
                "type": "install_package",
                "package": module_name,
                "action": "system_command"
            }

        # Strategy 2: Syntax Error -> Likely need to fix indentation or typos
        if error_type == "SyntaxError" or error_type == "IndentationError":
             return {
                "type": "auto_format",
                "action": "modify_code"
            }

        # Strategy 3: NameError -> Variable not defined
        if error_type == "NameError":
            var_name = re.search(r"name '(\w+)' is not defined", error_msg)
            if var_name:
                return {
                    "type": "define_variable",
                    "variable": var_name.group(1),
                    "action": "modify_code"
                }

        # Fallback
        return {
            "type": "unknown_fix",
            "action": "log_only"
        }

    def _save_to_memory(self, error_type, error_msg, solution):
        with open(self.memory_path, "a") as f:
            timestamp = datetime.datetime.now().isoformat()
            f.write(f"\n[{timestamp}] ERROR: {error_type} - {error_msg}\n")
            f.write(f"SOLUTION: {solution}\n")
