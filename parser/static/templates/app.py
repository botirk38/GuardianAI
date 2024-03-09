from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
@app.route('/ast_analysis', methods=['GET'])
def analyze_mock_ast():
    # This is a placeholder for the logic to compare the mock AST with known vulnerability patterns
    # For demonstration, we'll just return the mock ASTs
    return jsonify(mock_ast_vulnerabilities)

if __name__ == '__main__':
    app.run(debug=True)
