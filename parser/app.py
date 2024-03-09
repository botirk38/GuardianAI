from flask import Flask, jsonify



from ast_analysis.ast_mock_data import vulnerability_pattern, mock_submission_ast1 
from ast_analysis.ast_mock_data import mock_submission_ast2 , rawdata
from ast_analysis.ast_comparer import compare_ast
from ast_analysis.ast_simplfy import simplify_ast




app = Flask(__name__)

@app.route('/')
def hello_world():
    return test_analyze()


@app.route('/test_analyze', methods=['GET'])
def test_analyze():
    #found_vulnerabilities = compare_ast(mock_submission_ast1, vulnerability_pattern)
        vulnerability_found = compare_ast(mock_submission_ast1, vulnerability_pattern)
        simplified_ast = simplify_ast(rawdata)
        response_data = {
        "vulnerability_found": "yes" if vulnerability_found else "no",
        "simplified_ast": simplified_ast }
        answer = compare_ast(rawdata , vulnerability_pattern)
        print(answer)
        return jsonify(response_data)


    
    

if __name__ == '__main__':
    app.run(debug=True)
