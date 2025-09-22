import ast

def analyze_python_file(file_content):
    feedback = []
    try:
        tree = ast.parse(file_content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 50:
                    feedback.append(f"Function '{node.name}' is too long ({len(node.body)} lines)")
    except Exception:
        feedback.append("Failed to parse Python file.")

    for i, line in enumerate(file_content.splitlines(), 1):
        if len(line) > 120:
            feedback.append(f"Line {i} exceeds 120 characters")
    return feedback
