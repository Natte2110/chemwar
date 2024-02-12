from flask import render_template, request, redirect, flash, url_for, jsonify
from chemwar import app, db
from chemwar.models import User, Cordon, CBRN
import flask_login as fl
from hashlib import sha256
from datetime import datetime
from sqlalchemy import desc
import os

login_manager = fl.LoginManager(app)
login_manager.login_view = 'sign_in'
# PATH_TO_IMAGES = '/'.join(app.config['UPLOAD_FOLDER'].split("/")[-2:])

@login_manager.user_loader
def load_user(id):
    """Loads the current user and returns it as a query object.

    Arguments:
        id -- The id of the user, this will be used to search the
        USER database table for the corresponding entry.

    Returns:
        A User object returned from a query on the User table.
    """
    return User.query.get(int(id))

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

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    """Provides routing for the website's sign in page

    Returns:
        The sign-in.html page with the title of "Sign In"
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        # encrypted_password = sha256(password.encode("utf-8")).hexdigest()
        if user and (user.password == password):
            fl.login_user(user)
            # flash(f"Welcome {username}!")
            return redirect(url_for('home'))
        else:
            flash(f"User account not found.")
            return render_template("sign-in.html", title="Sign In")
    else:
        return render_template("sign-in.html", title="Sign In")

@app.route("/logout")
@fl.login_required
def logout():
    """Logs the user out of their account

    Returns:
        The home page.
    """
    fl.logout_user()
    return redirect(url_for('home'))