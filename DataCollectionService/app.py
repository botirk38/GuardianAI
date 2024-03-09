from flask import Flask, jsonify
from datasets import load_dataset
from models import RustCodeSample
import click
from flask.cli import with_appcontext
from settings import db, cache


def fetch_and_store_code_samples():
    ds = load_dataset("codeparrot/github-code", streaming=True, split="train")
    rust_samples = (sample for sample in ds if sample['language'] == 'Rust')

    for rust_sample in rust_samples:
        print(rust_sample)
        # Create a new database entry for each Rust code sample
        new_sample = RustCodeSample(
            repo_name=rust_sample['repo_name'],
            path=rust_sample['path'],
            code=rust_sample['code'],
            license=rust_sample['license'],
            size=rust_sample['size']
        )
        db.session.add(new_sample)
        # Commit every 100 samples to avoid keeping too many objects in session
        if RustCodeSample.query.count() % 100 == 0:
            db.session.commit()
    db.session.commit()  # Final commit for any remaining samples


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rust_codes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    cache.init_app(app)

    with app.app_context():
        db.create_all()

    @app.cli.command('populate-db')
    @with_appcontext
    def populate_db_command():
        """Populates the database with Rust code samples."""
        fetch_and_store_code_samples()
        click.echo("Database populated with Rust code samples.")

    @app.route("/fetch-code-sample", methods=['GET'])
    @cache.cached(timeout=60, key_prefix='rust_code_sample')
    def get_code_sample():

        try:

            sample = RustCodeSample.query.first()

            if sample:
                response = {
                    'repo_name': sample.repo_name,
                    'path': sample.path,
                    'code': sample.code,
                    'license': sample.license,
                    'size': sample.size

                }

                return jsonify(response)

            else:
                return jsonify({"error": "No code samples available"}), 404

        except Exception:
            return jsonify({"error": "Server error, please try again later."}), 500

    return app

    


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
