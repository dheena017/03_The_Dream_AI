
import subprocess
import os
import ast
import re

class Surgeon:
    """
    The Surgeon: Fixes the code based on Scholar's research.
    """

    def apply_fix(self, script_path, fix_plan):
        print(f"🩺 Surgeon: Operating on {script_path}...")

        if fix_plan['action'] == 'system_command':
            if fix_plan['type'] == 'install_package':
                package = fix_plan['package']
                print(f"🩺 Surgeon: Prescribing new library -> pip install {package}")
                try:
                    subprocess.check_call(['pip', 'install', package])
                    return True
                except Exception as e:
                    print(f"❌ Surgeon failed to install: {e}")
                    return False

        elif fix_plan['action'] == 'modify_code':
            return self._modify_file(script_path, fix_plan)

        return False

    def _modify_file(self, filepath, fix_plan):
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()

            new_lines = []
            modified = False

            if fix_plan['type'] == 'replace_import':
                original = fix_plan['original']
                replacement = fix_plan['replacement']
                print(f"🩺 Surgeon: Transplanting import {original} -> {replacement}")

                for line in lines:
                    indent = line[:len(line) - len(line.lstrip())]
                    if f"import {original}" in line:
                        new_lines.append(f"{indent}# Surgeon replaced broken import: {original}\n")
                        new_lines.append(f"{indent}import {replacement}\n")
                        modified = True
                    elif f"from {original}" in line:
                        new_lines.append(f"{indent}# Surgeon replaced broken import: {original}\n")
                        new_lines.append(line.replace(original, replacement))
                        modified = True
                    else:
                        new_lines.append(line)

            elif fix_plan['type'] == 'define_variable':
                # Crude fix: define variable as None at top
                var = fix_plan['variable']
                print(f"🩺 Surgeon: Injecting missing variable -> {var} = None")
                new_lines.append(f"{var} = None # Surgeon fixed NameError\n")
                new_lines.extend(lines)
                modified = True

            elif fix_plan['type'] == 'auto_format':
                print("🩺 Surgeon: Attempting auto-formatting with syntax fixers")
                new_lines = list(lines)

                try:
                    # Parse to find the first syntax error
                    full_source = "".join(new_lines)
                    ast.parse(full_source)
                except (SyntaxError, IndentationError) as e:
                    if e.lineno is not None:
                        line_idx = e.lineno - 1
                        if 0 <= line_idx < len(new_lines):
                            line = new_lines[line_idx]
                            original_line = line

                            # Fix 1: Unbalanced Brackets (Basic)
                            open_p = line.count('(')
                            close_p = line.count(')')
                            open_b = line.count('[')
                            close_b = line.count(']')
                            open_c = line.count('{')
                            close_c = line.count('}')

                            to_add = ""
                            if open_p > close_p: to_add += ')' * (open_p - close_p)
                            if open_b > close_b: to_add += ']' * (open_b - close_b)
                            if open_c > close_c: to_add += '}' * (open_c - close_c)

                            if to_add:
                                if line.endswith('\n'):
                                    line = line.rstrip('\r\n') + to_add + '\n'
                                else:
                                    line += to_add

                            # Fix 2: Missing Colon
                            colon_pattern = r'^\s*(async\s+)?(if|elif|else|for|while|def|class|try|except|finally|with)\b'
                            if re.match(colon_pattern, line) and not line.strip().endswith(':'):
                                if '#' in line:
                                    parts = line.split('#', 1)
                                    code_part = parts[0]
                                    comment_part = parts[1]
                                    if not code_part.strip().endswith(':'):
                                        line = code_part.rstrip() + ': #' + comment_part
                                else:
                                    line = line.rstrip() + ':\n'

                            if line != original_line:
                                new_lines[line_idx] = line
                                modified = True
                                print(f"🩺 Surgeon: Fixed syntax on line {e.lineno}")

                            # Fix 3: Indentation
                            if isinstance(e, IndentationError) and not modified:
                                new_lines[line_idx] = "    " + original_line
                                modified = True
                                print(f"🩺 Surgeon: Fixed indentation on line {e.lineno}")

                except Exception as e:
                    print(f"⚠️ Surgeon: analysis failed: {e}")

            if modified:
                with open(filepath, 'w') as f:
                    f.writelines(new_lines)
                print("✅ Surgeon: Operation successful.")
                return True
            else:
                print("⚠️ Surgeon: Could not find where to apply the fix.")
                return False

        except Exception as e:
            print(f"❌ Surgeon Error: {e}")
            return False
