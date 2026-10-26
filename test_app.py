import ast
from pathlib import Path

def test_app_has_valid_python_syntax():
    ast.parse(Path("app.py").read_text(encoding="utf-8"))

def test_required_functions_exist():
    tree = ast.parse(Path("app.py").read_text(encoding="utf-8"))
    functions = {
        node.name for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert "search_web" in functions
    assert "summarize_results" in functions
