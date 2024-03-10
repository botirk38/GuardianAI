from ast_mock_data import vulnerability_mapping, vulnerability_ranking


def getTotalPercentageFromMatrix(matrix):
    """
    This function returns weighted percentage of the matrix based on the vulnerability mapping and ranking.

    Args:
        matrix (list): The matrix to be analyzed.

    """

    percentage = 0
    total_elements = 0
    total_ranking = sum(vulnerability_ranking.values())
    vulnerable_elements = 0
    encountered_vulnerabilities = set()


    for row in matrix:
        for col in row:
            total_elements+=1
            if col in vulnerability_mapping.values():
                vulnerable_elements+=vulnerability_ranking[col]

    vulnerable_elements = (vulnerable_elements/total_ranking)* total_elements
    percentage = (vulnerable_elements/total_elements)*100
    return percentage

if __name__ == "__main__":
    matrix = [
        ['0001'],
        ['0010'],
        ['0011'],
        ['0100'],
        ['0101'],
        ['0110'],
        ['0111'],
        ['1000'],
        ['1001'],
        ['1010'],
        ['1011'],
        ['1100'],
        ['1101'],
        ['1110'],
        ['1111']
       
    ]

    print(getTotalPercentageFromMatrix(matrix))
