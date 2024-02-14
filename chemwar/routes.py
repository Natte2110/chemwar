from flask import render_template, request, redirect, flash, url_for, jsonify, session
from chemwar import app, db
from chemwar.models import Users, Cordons, CBRN, Groups, Reports
import flask_login as fl
from hashlib import sha256
from datetime import datetime
from sqlalchemy import desc
import os

login_manager = fl.LoginManager(app)
login_manager.login_view = 'sign_in'
current_sessions = {}
   
def get_user_group(id):
    return Groups.query.filter_by(id=id).first().name

@login_manager.user_loader
def load_user(id):
    """Loads the current user and returns it as a query object.

    Arguments:
        id -- The id of the user, this will be used to search the
        USER database table for the corresponding entry.

    Returns:
        A User object returned from a query on the User table.
    """
    
    return Users.query.get(int(id))

@app.route("/")
def home():
    """Provides routing for the website's home page

    Returns:
        The index.html page with the title of "Home"
    """
    
    if fl.current_user.is_authenticated:
        fl.current_user.group_name = get_user_group(fl.current_user.group)
        current_sessions[fl.current_user.id] = fl.current_user.username
    no_current_users = len(current_sessions)
    return render_template(
        "index.html", 
        title="Dashboard", 
        no_current_users=no_current_users,
        )

@app.route("/chemwar-viewer")
@fl.login_required
def chemwar_viewer():
    """Provides routing for the website's viewer page

    Returns:
        The index.html page with the title of "Viewer"
    """
    if fl.current_user.is_authenticated:
        fl.current_user.group_name = get_user_group(fl.current_user.group)
        current_sessions[fl.current_user.id] = fl.current_user.username
    return render_template("viewer.html", title="Viewer")

@app.route("/accounts", methods=["GET", "POST"])
@fl.login_required
def accounts():
    """Provides routing for the website's viewer page

    Returns:
        The index.html page with the title of "Viewer"
    """
    if fl.current_user.is_authenticated:
        fl.current_user.group_name = get_user_group(fl.current_user.group)
        current_sessions[fl.current_user.id] = fl.current_user.username
    if request.method == "POST":
        data = request.json
        username = data.get('username')
        print(data)
        if Users.query.filter_by(username=username).first() is None:
            try:
                user = Users(
                    username=username,
                    password=data.get('password'),
                    level=data.get('level'),
                    group=data.get('group'),
                    initial=data.get('initial'),
                    surname=data.get('surname'),
                    blood_group=data.get('blood_group'),
                    med_tag=data.get('med_tag')
                )
                db.session.add(user)
                db.session.commit()
            except:
                return jsonify({"success": False, "message":"Unkown Server Error"})
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message":"Username Already Exists"})
    else:
        if fl.current_user.level >= 2:
            return render_template(
                "accounts.html", 
                title="Accounts",
                users=Users.query.all(),
                groups=Groups.query.all()
                )
        else:
            no_current_users = len(current_sessions)
            return render_template(
            "index.html", 
            title="Dashboard", 
            no_current_users=no_current_users,
            )
        
@app.route("/delete-account", methods=["GET", "POST"])
@fl.login_required
def delete_account():
    if request.method == 'POST':
        data = request.json
        id = data.get('id')
        print(data)
        try:
            user_to_delete = Users.query.filter_by(id=id).first()
            db.session.delete(user_to_delete)
            db.session.commit()
        except:
            return jsonify({"success": False, "message":"Unkown Server Error"})
        return jsonify({"success": True})
    else:
        return redirect(url_for('home'))

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    """Provides routing for the website's sign in page

    Returns:
        The sign-in.html page with the title of "Sign In"
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username).first()
        # encrypted_password = sha256(password.encode("utf-8")).hexdigest()
        if user and (user.password == password):
            fl.login_user(user)
            # flash(f"Welcome {username}!")
            current_sessions[fl.current_user.id] = fl.current_user.username
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
    current_sessions.pop(fl.current_user.id)
    fl.logout_user()
    return redirect(url_for('home'))