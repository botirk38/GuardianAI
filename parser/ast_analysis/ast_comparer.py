

def traverse_and_compare(node, patterns):
    found_vulnerabilities = []
    
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
    vulnerabilities_found = traverse_and_compare(submitted_ast, vulnerability_patterns)

    if vulnerabilities_found:
        for vulnerability in vulnerabilities_found:
            print(f"Vulnerability found: {vulnerability[0]} in context: {vulnerability[1]}")
            return vulnerabilities_found
    else:
        print("No vulnerabilities found.")

