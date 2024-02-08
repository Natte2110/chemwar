from flask import render_template, request, redirect, flash, url_for, jsonify
from chemwar import app, db
# from chemwar.models import User, Category, Post, Reaction, Comment
# import flask_login as fl
from hashlib import sha256
from datetime import datetime
from sqlalchemy import desc
import os

# login_manager = fl.LoginManager(app)
# login_manager.login_view = 'log_in'
# PATH_TO_IMAGES = '/'.join(app.config['UPLOAD_FOLDER'].split("/")[-2:])

@app.route("/")
def home():
    """Provides routing for the website's home page

    Returns:
        The index.html page with the title of "Home"
    """
    return render_template("index.html", title="Home")

@app.route("/chemwar-viewer")
def chemwar_viewer():
    """Provides routing for the website's viewer page

    Returns:
        The index.html page with the title of "Viewer"
    """
    return render_template("viewer.html", title="Viewer")

