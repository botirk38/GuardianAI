from flask import jsonify


from ast_analysis.ast_mock_data import vulnerability_pattern, mock_submission_ast1 
from ast_analysis.ast_mock_data import mock_submission_ast2
from ast_analysis.ast_comparer import compare_ast
from ast_analysis.ast_simplfy import simplify_ast, fetch_ast
from settings import app



@app.cli.command("populate_db")
def fetch_ast():
    """Fetches AST and populates the database."""
    url = "http://localhost:8080//processing-service/process-code/rust"

    try:
        response = requests.get(url)
            
        if response.status_code == 200:
            data = response.json()
            print("Data:", data)
            db.session.add(data)
            db.session.commit()

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
        simplified_ast = simplify_ast(raw_data)
        response_data = {
        "simplified_ast": simplified_ast }
        answer = compare_ast(raw_data , vulnerability_pattern)
        print(answer)
        return jsonify(response_data)


    
    

if __name__ == '__main__':
    app.run(debug=True)
    
