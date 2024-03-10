from flask import Flask, jsonify



from ast_analysis.ast_mock_data import vulnerability_pattern  
from ast_analysis.ast_mock_data import mock_ast , rawdata
from ast_analysis.ast_comparer import compare_ast
from ast_analysis.ast_simplfy import simplify_ast
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
            "vulnerability_found": "yes",
            "matrix": vulnerability_found
        }
    else:
        response_data = {
            "vulnerability_found": "no",
            "matrix": []
        }

    # Return the response data as JSON
    return jsonify(response_data)


    
    

if __name__ == '__main__':
    app.run(debug=True)
