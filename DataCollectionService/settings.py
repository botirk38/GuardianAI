from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache',
              'CACHE_DEFAULT_TIMEOUT': 300})

app = Flask(__name__)
