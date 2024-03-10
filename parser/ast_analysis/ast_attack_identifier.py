def get_attack_descriptions(binary_vulnerabilities, attack_mapping):
    descriptions = [attack_mapping.get(binary[0], "Unknown vulnerability.") for binary in binary_vulnerabilities]
    return descriptions
