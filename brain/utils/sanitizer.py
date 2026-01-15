import re
import sys
import ast
from pathlib import Path

def is_valid_python(content):
    """Checks if the code is valid Python using the AST parser."""
    try:
        ast.parse(content)
        return True
    except SyntaxError:
        return False

def sanitize_file(filepath):
    """
    Reads a file and attempts to fix common AI generation errors:
    1. Removes Markdown code blocks (```python ... ```)
    2. Trims conversational text appended to the end.
    3. Removes natural language appended after code
    """
    path = Path(filepath)
    if not path.exists():
        return False
        
    try:
        content = path.read_text(encoding='utf-8')
    except Exception:
        return False # file might be locked or binary

    # 1. If it's already valid Python, do nothing.
    if is_valid_python(content):
        return False

    original_content = content
    print(f"⚠️  Syntax Error detected in {path.name}. Attempting surgery...")

    # 2. Strategy: Extract code from Markdown blocks
    # AI often wraps code in ```python ... ```
    pattern = r"```(?:python)?\s*(.*?)```"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        clean_code = match.group(1).strip()
        if is_valid_python(clean_code):
            path.write_text(clean_code, encoding='utf-8')
            print("✨ Fixed via Markdown extraction.")
            return True

    # 3. Strategy: Aggressive Tail Trimming
    # AI often adds "Hope this helps!" at the end, breaking the code.
    # We remove lines from the bottom until it parses correctly.
    lines = content.splitlines()
    # Don't trim if file is too short (safety)
    if len(lines) > 5:
        for i in range(len(lines), 1, -1):
            # Try the file without the last i lines
            candidate = "\n".join(lines[:i])
            if is_valid_python(candidate):
                path.write_text(candidate, encoding='utf-8')
                print(f"✂️  Amputated {len(lines) - i} lines of garbage text.")
                return True
    
    # 4. Strategy: Remove conversational text at the end
    # Sometimes AI appends explanations without code blocks
    # Find where the natural language starts
    lines = content.splitlines()
    for i in range(len(lines) - 1, 0, -1):
        candidate = "\n".join(lines[:i])
        # Skip empty or comment-only lines
        non_comment_lines = [l for l in candidate.splitlines() 
                             if l.strip() and not l.strip().startswith('#')]
        if non_comment_lines and is_valid_python(candidate):
            if len(lines) - i > 1:
                path.write_text(candidate, encoding='utf-8')
                print(f"🧹 Removed {len(lines) - i} lines of conversational text.")
                return True
    
    # If nothing worked, file is too broken
    print(f"❌ Could not fix {path.name} - too many syntax errors")
    return False
