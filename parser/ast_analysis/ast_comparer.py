def traverse_and_compare(node, pattern):
    if matches_pattern(node, pattern):
        return True

    for key, value in node.items():
        if isinstance(value, dict):
            if traverse_and_compare(value, pattern):
                return True
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and traverse_and_compare(item, pattern):
                    return True

    return False

def matches_pattern(node, pattern):

    #print (" this is node type " + node.get("type") + " " + pattern.get("type"))
    print("this is node type " + node.get("type", "unknown"))
    if (node.get("type") == ("MethodCall")):
        if ((node.get("method")) == (pattern.get("type"))):
            return True

def compare_ast(submitted_ast, vulnerability_pattern):
    print("hi")
    return traverse_and_compare(submitted_ast, vulnerability_pattern)
