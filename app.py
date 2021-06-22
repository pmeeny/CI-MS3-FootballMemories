import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

UPLOAD_FOLDER = '/workspace/CI-MS3-FootballMemories/static/images'
IMAGE_PATH = '/static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_PATH'] = IMAGE_PATH

mongo = PyMongo(app)

@app.route("/")
@app.route("/get_memories")
def get_memories():
    memories = mongo.db.memories.find()
    return render_template("memories.html", memories=memories)

@app.route("/get_memory/<id>")
def get_memory(id):
    memory = mongo.db.memories.find_one({"_id": ObjectId(id)})
    print(id)
    comments = mongo.db.comments.find({"memory_id":  id})
    return render_template("memory.html", memory=memory, comments=comments)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
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
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
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
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    return render_template("profile.html", username=username)

@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))

@app.route("/get_tournaments")
def get_tournaments():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    tournaments = list(mongo.db.tournaments.find().sort("tournament_name", 1))
    pagination = Pagination(page=page, total=5, search=search, record_name='tournament_name')
    return render_template("tournament.html", tournaments=tournaments, pagination=pagination)
    
@app.route("/add_tournament", methods=["GET", "POST"])
def add_tournament():
    if request.method == "POST":
        tournament = {
            "tournament_name": request.form.get("tournament_name")
        }
        mongo.db.tournaments.insert_one(tournament)
        flash("New tournament Added")
        return redirect(url_for("get_tournaments"))

    return render_template("add_tournament.html")

@app.route("/edit_tournament/<tournament_id>", methods=["GET", "POST"])
def edit_tournament(tournament_id):
    if request.method == "POST":
        submit = {
            "tournament_name": request.form.get("tournament_name")
        }
        mongo.db.tournaments.update({"_id": ObjectId(tournament_id)}, submit)
        flash("Tournament Successfully Updated")
        return redirect(url_for("get_tournaments"))

    tournament = mongo.db.tournaments.find_one({"_id": ObjectId(tournament_id)})
    return render_template("edit_tournament.html", tournament=tournament)

@app.route("/delete_tournament/<tournament_id>")
def delete_tournament(tournament_id):
    mongo.db.tournaments.remove({"_id": ObjectId(tournament_id)})
    flash("Tournament Successfully Deleted")
    return redirect(url_for("get_tournaments"))

@app.route("/add_memory", methods=["GET", "POST"])
def add_memory():
    if request.method == "POST":
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path_to_image = (os.path.join(
        app.config['IMAGE_PATH'], filename))

        memory = {
            "image": path_to_image,
            "tournament_name": request.form.get("tournament_name"),
            "memory_name": request.form.get("memory_name"),
            "memory_description": request.form.get("memory_description"),
            "created_by": session["user"]
        }
        mongo.db.memories.insert_one(memory)
        flash("Memory Successfully Added")
        return redirect(url_for("get_memories"))

    tournaments = mongo.db.tournaments.find().sort("tournament_name", 1)
    return render_template("add_memory.html", tournaments=tournaments)

@app.route("/add_comment/<memory>/<id>", methods=["POST"])
def add_comment(memory, id):
    now = datetime.now() # current date and time
    year = now.strftime("%Y")
    month = now.strftime("%m")
    print(session)
    comment = {
        "memory_id": id,
        "comment_text": request.form.get("comment"),
        "comment_date": month + "-" + year,
        "created_by": session["user"]
    }
    mongo.db.comments.insert_one(comment)
    flash("Comment Successfully Added")
    comments = mongo.db.comments.find({"memory_id":  id})

    return render_template("memory.html", memory=memory, comments=comments)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)