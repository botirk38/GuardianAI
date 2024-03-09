def traverse_and_compare(node, pattern):

    if isinstance(node, dict):
        if matches_pattern(node, pattern):
            return True
        # Recursively call on each value
        for key, value in node.items():
            if traverse_and_compare(value, pattern):
                return True


    elif isinstance(node, list):
        return any(traverse_and_compare(item, pattern) for item in node)

    
    return False

def matches_pattern(node, pattern):
    node_type = node.get("type") or node.get("name")
    print("this is node type:", node_type)

    # Adjust the pattern matching to use "name" as "type" if necessary
    expected_type = pattern.get("type")

    if node_type == expected_type:
        return True
    return False


def compare_ast(submitted_ast, vulnerability_pattern):
    print("Searching for vulnerabilities...")
    return traverse_and_compare(submitted_ast, vulnerability_pattern)
