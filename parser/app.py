from flask import Flask, jsonify, request
import requests
from ast_analysis.ast_mock_data import vulnerability_pattern
from ast_analysis.ast_mock_data import mock_ast, rawdata
from ast_analysis.ast_comparer import compare_ast
from ast_analysis.ast_simplfy import simplify_ast, fetch_ast, post_code
from ast_analysis.ast_mock_data import attack_mapping
from ast_analysis.build_percentage import get_total_percentage
from flask_cors import CORS
from flask.cli import with_appcontext
import click
import csv

app = Flask(__name__)
CORS(app)

@app.cli.command("build_csv")
@click.argument('filename')
@with_appcontext
def build_csv(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for _ in range(1):
            data = fetch_ast()
            print("Data:", data)
            if data:
                ast = data.get('Tree:')
                print("AST:", ast)  
                code_sample = data.get('Code:')
                print("Code sample:", code_sample)
                normalized_ast = simplify_ast(ast)
                if normalized_ast:
                    vulnerability_matrix = compare_ast(normalized_ast, vulnerability_pattern)
                    if vulnerability_matrix:
                        for row in vulnerability_matrix:
                            writer.writerow(row + [code_sample])

    click.echo(f'CSV file {filename} has been created.')
    return filename



def fetch_ast():
    """Fetches AST and populates the database."""
    url = "http://localhost:8080/processing-service/process-code/rust"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # db.session.add(data)
            # db.session.commit()

            return data

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
    print("AST:", ast)

    

    if ast:
        # Simplify the AST
        simplified_ast = simplify_ast(ast)

        # Compare the simplified AST with the vulnerability pattern

        vulnerability_matrix = compare_ast(
            simplified_ast, vulnerability_pattern)

        print("Vulnerability matrix:", vulnerability_matrix)

        # potential_attacks =  determine_potential_attacks(vulnerability_matrix)

        # Calculate the percentage of vulnerabilities in the code

        percentage = get_total_percentage(vulnerability_matrix)

        # If vulnerabilities are found, format them into a response

        return jsonify({
            "percentage": percentage,
            "simplifiedAST": simplified_ast,
        })

    return jsonify({
        "error": "Failed to fetch AST"
    })


if __name__ == '__main__':
    app.run(debug=True)
