def traverse_and_compare(node, pattern):
    if matches_pattern(node, pattern):
        return True

    for child in node.get("body", []):
        print("hi")
        if traverse_and_compare(child, pattern):
            return True
    
    return False

def matches_pattern(node, pattern):
    print (" this is node type " + node.get("type") + " " + pattern.get("type"))
    return node.get("type") == pattern.get("type")

def compare_ast(submitted_ast, vulnerability_pattern):
    return traverse_and_compare(submitted_ast, vulnerability_pattern)
