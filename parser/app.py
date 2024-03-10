from flask import Flask, jsonify, request
import requests
from ast_analysis.ast_mock_data import vulnerability_pattern
from ast_analysis.ast_mock_data import mock_ast, rawdata
from ast_analysis.ast_comparer import compare_ast
from ast_analysis.ast_simplfy import simplify_ast, fetch_ast, post_code
from ast_analysis.ast_mock_data import attack_mapping
from settings import app
from ast_analysis.build_percentage import get_total_percentage


@app.cli.command("populate_db")
def fetch_ast():
    """Fetches AST and populates the database."""
    url = "http://localhost:8080/processing-service/process-code/rust"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print("Data:", data)
            # db.session.add(data)
            # db.session.commit()

        else:
            print(f"Failed to fetch AST: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(e)
        return None


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


@app.route("/analyze-code", methods=["POST"])
def analyze_code():
    # Fetch the AST from the code processing service
    form_data = request.json
    print("Form data:", form_data)
    ast = post_code(form_data)

    

    if ast:
        # Simplify the AST
        simplified_ast = simplify_ast(rawdata)
        print("Simplified AST:", simplified_ast)

        # Compare the simplified AST with the vulnerability pattern

        vulnerability_matrix = compare_ast(
            simplified_ast, vulnerability_pattern)

        print("Vulnerability matrix:", vulnerability_matrix)

        # potential_attacks =  determine_potential_attacks(vulnerability_matrix)

        # Calculate the percentage of vulnerabilities in the code

        percentage = get_total_percentage(vulnerability_matrix)

        # If vulnerabilities are found, format them into a response

        return jsonify({
            "percentage": percentage
        })

    return jsonify({
        "error": "Failed to fetch AST"
    })


if __name__ == '__main__':
    app.run(debug=True)
