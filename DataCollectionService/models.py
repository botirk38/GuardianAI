from settings import db


class RustCodeSample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    code = db.Column(db.Text, nullable=False)
    license = db.Column(db.String, nullable=True)
    size = db.Column(db.Integer, nullable=False)
