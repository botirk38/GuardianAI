def map_vulnerabilities_to_binary(vulnerabilities_found, vulnerability_mapping):
    binary_values = []
    for vuln_type, _ in vulnerabilities_found:
        binary_value = vulnerability_mapping.get(vuln_type, '0000')
        binary_values.append([binary_value])
    return binary_values