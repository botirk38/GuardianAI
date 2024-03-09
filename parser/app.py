from flask import jsonify


from ast_analysis.ast_mock_data import vulnerability_pattern, mock_submission_ast1 
from ast_analysis.ast_mock_data import mock_submission_ast2
from ast_analysis.ast_comparer import compare_ast
from ast_analysis.ast_simplfy import simplify_ast, fetch_ast
from settings import app






@app.route('/')
def hello_world():
    return test_analyze()


@app.route('/test_analyze', methods=['GET'])
def test_analyze():
        raw_data = fetch_ast()
        simplified_ast = simplify_ast(raw_data)
        response_data = {
        "simplified_ast": simplified_ast }
        answer = compare_ast(raw_data , vulnerability_pattern)
        print(answer)
        return jsonify(response_data)


    
    

if __name__ == '__main__':
    app.run(debug=True)
