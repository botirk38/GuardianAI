from mock_ast_data import vulnerability_pattern , mock_submission_ast1

node =  mock_submission_ast1
pattern = vulnerability_pattern

def compare_ast( node , pattern):
    """
    Recursively traverses the AST node and its children, comparing against a vulnerability pattern.
    """
    if matches_pattern(node, pattern):
        print(f"Vulnerability found at line: {node.get('line', 'N/A')}")
        return True

    for child in node.get("children", []):
        if compare_ast(child, pattern):
            return True
    
    return False

def matches_pattern(node, pattern):
    """
    Checks if the current node matches the vulnerability pattern.
    """
    return node.get("type") == pattern.get("type")

