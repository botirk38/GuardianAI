from ast_analysis.ast_matrix_builder import map_vulnerabilities_to_binary
from ast_analysis.ast_mock_data import vulnerability_mapping

def traverse_and_compare(node, patterns):
    found_vulnerabilities = []
    binary_vulnerabilities = []


    
    if isinstance(node, dict):
        for pattern in patterns:
            if node.get("type") == pattern.get("type"):
                found_vulnerabilities.append((node.get("type"), node.get("parentType")))
                break  # Break to avoid duplicate reporting

        for value in node.values():
            found_vulnerabilities.extend(traverse_and_compare(value, patterns))

    elif isinstance(node, list):
        for item in node:
            found_vulnerabilities.extend(traverse_and_compare(item, patterns))

    return found_vulnerabilities

def compare_ast(submitted_ast, vulnerability_patterns):
    print("Searching for vulnerabilities...")
    vulnerabilities_found = traverse_and_compare(submitted_ast["simplified_ast"]["children"], vulnerability_patterns)

    if vulnerabilities_found:
        binary_vulnerabilities = map_vulnerabilities_to_binary(vulnerabilities_found, vulnerability_mapping)
        for vulnerability in vulnerabilities_found:
            print(f"Vulnerability found: {vulnerability[0]} in context: {vulnerability[1]}")
            return binary_vulnerabilities
        for binary in binary_vulnerabilities:
            print(f"Binary Vulnerability: {binary}")
    else:
        print("No vulnerabilities found.")
        binary_vulnerabilities = [['0000']]

    return binary_vulnerabilities

