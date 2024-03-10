

#def map_vulnerabilities_to_binary(vulnerabilities_found, vulnerability_mapping):
 #   binary_values = [vulnerability_mapping[vuln[0]] for vuln in vulnerabilities_found if vuln[0] in vulnerability_mapping]
  #  return binary_values

def map_vulnerabilities_to_binary(vulnerabilities_found, vulnerability_mapping):
    binary_values = []
    for vuln_type, _ in vulnerabilities_found:
        # Use the mapped binary value if the vulnerability type is recognized; otherwise, use '0000'
        binary_value = vulnerability_mapping.get(vuln_type, '0000')
        binary_values.append([binary_value])
    return binary_values