import ast
import os

class CodeAnalyzer:
    """Reads Python source code and analyzes its structure."""
    
    def analyze_file(self, filepath):
        """
        Parses a file and returns complexity metrics.
        """
        if not os.path.exists(filepath):
            return {"error": f"File not found: {filepath}"}
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Parse the code into an Abstract Syntax Tree (AST)
            tree = ast.parse(source)
        except Exception as e:
            return {"error": f"Syntax/Read Error: {e}"}

        # Count structural elements
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        loops = [node for node in ast.walk(tree) if isinstance(node, (ast.For, ast.While))]
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        
        # Calculate a simple "Complexity Score"
        lines = len(source.splitlines())
        complexity_score = len(functions) + len(classes) + (len(loops) * 2)

        return {
            "filepath": filepath,
            "lines_of_code": lines,
            "functions": len(functions),
            "classes": len(classes),
            "loops": len(loops),
            "imports": len(imports),
            "complexity_score": complexity_score,
            "can_optimize": len(loops) > 0
        }














































# ✅ Reviewed by AI - 2026-01-14T14:17:26.826673Z
# Complexity: 2 | Status: OPTIMAL


# ✅ Reviewed by AI - 2026-01-14T14:17:28.324670Z
# Complexity: 2 | Status: OPTIMAL


# ✅ Reviewed by AI - 2026-01-14T14:17:32.083018Z
# Complexity: 2 | Status: OPTIMAL
