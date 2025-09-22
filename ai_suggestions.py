def ai_suggest(file_content):
    suggestions = []
    if "print(" in file_content:
        suggestions.append("Consider using logging instead of print for production code.")
    if "eval(" in file_content:
        suggestions.append("Avoid using eval() – it can be unsafe.")
    return suggestions
