from flask import Flask, jsonify
import requests
from ast_analysis.ast_mock_data import vulnerability_pattern  
from ast_analysis.ast_mock_data import mock_ast , rawdata
from ast_analysis.ast_comparer import compare_ast
from ast_analysis.ast_simplfy import simplify_ast
from ast_analysis.ast_mock_data import attack_mapping
from settings import app






@app.route('/')
def hello_world():
    return test_analyze()


@app.route('/test_analyze', methods=['GET'])
def test_analyze():
    vulnerability_found = compare_ast(mock_ast, vulnerability_pattern)

    
    # If vulnerabilities are found, format them into a response
    if vulnerability_found:
        response_data = {
            "MATRIX": vulnerability_found
        }
    else:
        response_data = {
            "vulnerability_found": "no",
            "matrix": []
        }

    # Return the response data as JSON
    return jsonify(response_data)

@app.route("/analyze-code", methods=['POST'])
def analyze_code(form_data):
    # Fetch the AST from the code processing service
    ast = post_code(form_data)

    if ast:
        # Simplify the AST
        simplified_ast = simplify_ast(ast)

        # Compare the simplified AST with the vulnerability pattern

        vulnerability_matrix = compare_ast(simplified_ast, vulnerability_pattern)

        potential_attacks =  determine_potential_attacks(vulnerability_matrix)

        # Calculate the percentage of vulnerabilities in the code

        percentage = getTotalPercentageFromMatrix(vulnerability_matrix)


        # If vulnerabilities are found, format them into a response

        return jsonify({
            "potential_attacks": potential_attacks,
            "percentage": percentage
        })

    return jsonify({
        "error": "Failed to fetch AST"
    })
    



            


            







    
    

if __name__ == '__main__':
    app.run(debug=True)
