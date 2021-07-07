from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, Blueprint, session,abort)

from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import current_app
from football_memories import mongo

authentication = Blueprint('authentication', __name__)

@authentication.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("authentication.register"))

        register = {
            "user_type": "regular_user",
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "favourite_team": request.form.get("favourite_team"), 
            "country": request.form.get("country")                     
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("memories.get_memories", username=session["user"]))

    return render_template("authentication/register.html")

@authentication.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "memories.get_memories", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("authentication.login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("authentication.login"))

    return render_template("authentication/login.html")

@authentication.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("administration.home"))

@authentication.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    user = mongo.db.users.find_one({"username": username})
    return render_template("authentication/profile.html", username=session['user'], user=user)


@authentication.route("/update_profile/<username>", methods=["GET", "POST"])
def update_profile(username):
    if request.method == "POST":
        update_profile = {
            "user_type": "regular_user",
            "username": session['user'],
            "password": generate_password_hash(request.form.get("password")),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "favourite_team": request.form.get("favourite_team"), 
            "country": request.form.get("country")     
        }
        mongo.db.users.update({"username": username}, update_profile)
        flash("User Profile Successfully Updated")

    user = mongo.db.users.find_one({"username": username})    
    return render_template("authentication/profile.html", username=session['user'], user=user)   