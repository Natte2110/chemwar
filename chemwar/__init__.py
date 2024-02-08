import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
if os.path.exists("env.py"):
    import env  # noqa


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
# app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER")
db = SQLAlchemy(app)

from chemwar import routes  # noqa