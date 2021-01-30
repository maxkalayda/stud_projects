from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from os import path

basedir = path.abspath(path.join(path.dirname(__file__), '..', 'sv_packages/templates'))
app = Flask(__name__)
app.secret_key = 'my supersecret key of all apps'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/login_params.db'
app.config['SQLALCHEMY_BINDS'] = {
    'main': 'sqlite:///database/sqlite.db'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from sv_packages import routes

db.create_all()
