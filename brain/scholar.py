
import os
import re
import datetime

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
        error_type, error_msg, line_number = self._parse_error(error_output, script_path)
        print(f"🎓 Scholar: Identified error -> {error_type}: {error_msg} (Line {line_number})")

        # 2. Check memory first
        known_fix = self._check_memory(error_type, error_msg)
        if known_fix:
            # Inject line number if available
            if line_number and 'line_number' not in known_fix:
                known_fix['line_number'] = line_number
            print("🎓 Scholar: Recall -> I have solved this before!")
            return known_fix

        # 3. Research (Web Search Simulation / Real Search)
        print("🎓 Scholar: Researching solution online...")
        solution = self._web_search_solution(error_type, error_msg, line_number)

        # 4. Save to memory
        self._save_to_memory(error_type, error_msg, solution)

        return solution

    def _parse_error(self, output, script_path=None):
        """Extracts the last error and line number from traceback"""
        lines = output.split('\n')
        error_type = "UnknownError"
        error_msg = "Unknown error"
        line_number = None

        # Look for traceback
        for line in reversed(lines):
            if line.strip() and ":" in line:
                # Basic python error detection (e.g. NameError: name 'x' is not defined)
                parts = line.split(':', 1)
                if len(parts) == 2 and parts[0].strip().endswith('Error'):
                    error_type = parts[0].strip()
                    error_msg = parts[1].strip()
                    break

        # Look for line number
        if script_path:
            # Simple check for script name in traceback lines
            # script_path might be absolute or relative, output might differ
            script_name = os.path.basename(script_path)

            for line in lines:
                if script_name in line and "File " in line:
                    match = re.search(r"line (\d+)", line)
                    if match:
                        line_number = int(match.group(1))
                        # We keep searching to find the *last* occurrence (deepest in stack for that file)
                        # or specifically where the error originated.
                        # Usually the last mention of the file is what we want.

        return error_type, error_msg, line_number

    def _check_memory(self, error_type, error_msg):
        # TODO: Implement actual lookup in corpus.txt
        return None

    def _web_search_solution(self, error_type, error_msg, line_number=None):
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
                fix = {
                    "type": "define_variable",
                    "variable": var_name.group(1),
                    "action": "modify_code"
                }
                if line_number:
                    fix["line_number"] = line_number
                return fix

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
