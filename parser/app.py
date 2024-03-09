from flask import Flask, jsonify



from ast_analysis.ast_mock_data import vulnerability_pattern, mock_submission_ast1
from ast_analysis.ast_comparer import compare_ast



app = Flask(__name__)

@app.route('/')
def hello_world():
    return test_analyze()

@app.route('/test_analyze', methods=['GET'])
def test_analyze():
    #found_vulnerabilities = compare_ast(mock_submission_ast1, vulnerability_pattern)
    if compare_ast(mock_submission_ast1, vulnerability_pattern) == True:
        return "yes"
    else:
        return "no"
    

if __name__ == '__main__':
    app.run(debug=True)
