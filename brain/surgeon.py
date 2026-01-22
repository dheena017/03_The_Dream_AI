
import subprocess
import os

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
                var = fix_plan['variable']
                line_number = fix_plan.get('line_number')

                if line_number and isinstance(line_number, int) and 0 < line_number <= len(lines):
                    # Smart fix: define variable before usage with correct indentation
                    target_index = line_number - 1
                    target_line = lines[target_index]

                    # Detect indentation
                    indent = target_line[:len(target_line) - len(target_line.lstrip())]
                    # Clean line (remove comments and whitespace)
                    stripped_line = target_line.split('#')[0].strip()

                    # Safety Check: Avoid injecting inside multi-line expressions if possible
                    # Heuristics:
                    # 1. Ends with ',' -> likely list/tuple/arg list
                    # 2. Ends with '\' -> continuation
                    # 3. Starts with closing bracket/brace
                    is_unsafe = (
                        stripped_line.endswith(',') or
                        stripped_line.endswith('\\') or
                        stripped_line.startswith(')') or
                        stripped_line.startswith(']') or
                        stripped_line.startswith('}')
                    )

                    if is_unsafe:
                        print(f"🩺 Surgeon: Line {line_number} looks unsafe for injection (inside expression?). Falling back to crude fix.")
                        # Crude fix fallback
                        print(f"🩺 Surgeon: Injecting missing variable -> {var} = None (at top)")
                        new_lines.append(f"{var} = None # Surgeon fixed NameError\n")
                        new_lines.extend(lines)
                        modified = True
                    else:
                        print(f"🩺 Surgeon: Injecting missing variable -> {var} = None at line {line_number}")

                        # Reconstruct lines
                        new_lines = lines[:target_index]
                        new_lines.append(f"{indent}{var} = None # Surgeon fixed NameError\n")
                        new_lines.extend(lines[target_index:])
                        modified = True
                else:
                    # Crude fix: define variable as None at top (Fallback)
                    print(f"🩺 Surgeon: Injecting missing variable -> {var} = None (at top)")
                    new_lines.append(f"{var} = None # Surgeon fixed NameError\n")
                    new_lines.extend(lines)
                    modified = True

            elif fix_plan['type'] == 'auto_format':
                # Just reading and writing might not fix syntax,
                # but maybe we can use a formatter if available?
                # For now, let's just assume we can't easily fix syntax without an LLM.
                print("🩺 Surgeon: Attempting auto-formatting (not fully implemented)")
                new_lines = lines
                # TODO: Implement basic syntax fixers (brackets, colons)

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
