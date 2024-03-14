from ast_analysis.ast_comparer import compare_ast
from flask.cli import with_appcontext
import click
from ast_analysis.ast_simplfy import fetch_ast, simplify_ast
from ast_analysis.ast_mock_data import vulnerability_pattern
import csv

@app.cli.command("build_csv")
@with_appcontext
def build_csv(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for _ in range(10000):
            data = fetch_ast()
            if data:
                ast = data.get('Tree: ')
                code_sample = data.get('Code: ')
                normalized_ast = simplify_ast(ast)
                if normalized_ast:
                    vulnerability_matrix = compare_ast(normalized_ast, vulnerability_pattern)
                    if vulnerability_matrix:
                        for row in vulnerability_matrix:
                            writer.writerow(row + [code_sample])

    click.echo(f'CSV file {filename} has been created.')
    return filename



    


