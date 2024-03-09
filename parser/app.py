from flask import Flask, jsonify
import sys


from ast_analysis.mock_ast_data import vulnerability_pattern, mock_submission_ast1
from ast_analysis.ast_comparer import compare_ast

app = Flask(__name__)

@app.route('/')
def hello_world():
    print('Hello, World!')
    return test_analyze()

@app.route('/test_analyze', methods=['GET'])
def test_analyze():

    found_vulnerabilities = compare_ast(mock_submission_ast1, vulnerability_pattern)

    return found_vulnerabilities

if __name__ == '__main__':
    app.run(debug=True)
