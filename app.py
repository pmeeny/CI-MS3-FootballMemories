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
from flask_paginate import Pagination, get_page_args

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

    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page',
        offset_parameter='offset')

    per_page = 3
    offset = (page - 1) * 3

    total_memories = mongo.db.memories.find().count()
    memories = mongo.db.memories.find()
    memories_paginated = memories[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_memories, css_framework='bootstrap')

    return render_template("memories.html", memories=memories_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@app.route("/get_user_memories")
def get_user_memories():
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page',
        offset_parameter='offset')

    per_page = 3
    offset = (page - 1) * 3

    username = session["user"]

    total_user_memories = mongo.db.memories.find({"created_by": username}).count()
    user_memories = mongo.db.memories.find({"created_by": username})
    user_memories_paginated = user_memories[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_user_memories, css_framework='bootstrap')

    return render_template("memories.html", memories=user_memories_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@app.route("/get_memory/<id>")
def get_memory(id):

    page, per_page, offset = get_page_args(
    page_parameter='page', per_page_parameter='per_page',
    offset_parameter='offset')

    per_page = 6
    offset = (page - 1) * 6

    memory = mongo.db.memories.find_one({"_id": ObjectId(id)})

    comments = mongo.db.comments.find({"memory_id":  id})
    total_comments = mongo.db.comments.find({"memory_id":  id}).count()
    comments_paginated = comments[offset: offset + per_page]

    pagination = Pagination(page=page, per_page=per_page,
                            total=total_comments, css_framework='bootstrap')

    return render_template("memory.html", memory=memory, comments=comments_paginated, page=page,
                           per_page=per_page,
                           pagination=pagination)

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
                            "get_memories", username=session["user"]))
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

    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page',
        offset_parameter='offset')

    per_page = 3
    offset = (page - 1) * 3

    total_tournaments = mongo.db.tournaments.find().count()
    tournaments = list(mongo.db.tournaments.find().sort("tournament_name", 1))
    tournaments_paginated = tournaments[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_tournaments, css_framework='bootstrap')

    return render_template("tournament.html", tournaments=tournaments_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)
    
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
            "date": request.form.get("date"),
            "stadium": request.form.get("stadium"),
            "created_by": session["user"]
        }
        mongo.db.memories.insert_one(memory)
        flash("Memory Successfully Added")
        return redirect(url_for("get_memories"))

    tournaments = mongo.db.tournaments.find().sort("tournament_name", 1)
    return render_template("add_memory.html", tournaments=tournaments)

@app.route("/edit_memory/<memory_id>", methods=["GET", "POST"])
def edit_memory(memory_id):
    
    if request.method == "POST":
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path_to_image = (os.path.join(
        app.config['IMAGE_PATH'], filename))
        memory_to_update = {
            "image": path_to_image,
            "tournament_name": request.form.get("tournament_name"),
            "memory_name": request.form.get("memory_name"),
            "memory_description": request.form.get("memory_description"),
            "date": request.form.get("date"),
            "stadium": request.form.get("stadium"),
            "created_by": session["user"]
        }
        mongo.db.memories.update({"_id": ObjectId(memory_id)}, memory_to_update)
        flash("Memory Successfully Updated")
        return redirect(url_for("get_user_memories"))

    memory = mongo.db.memories.find_one({"_id": ObjectId(memory_id)})
    tournaments = mongo.db.tournaments.find().sort("tournament_name", 1)
    return render_template("edit_memory.html", memory=memory, tournaments=tournaments)


@app.route("/delete_memory/<memory_id>")
def delete_memory(memory_id):
    mongo.db.memories.remove({"_id": ObjectId(memory_id)})
    flash("Memory Successfully Deleted")
    return redirect(url_for("get_memories"))

@app.route("/add_comment/<id>", methods=["POST"])
def add_comment(id):
    now = datetime.now() # current date and time
    year = now.strftime("%Y")
    month = now.strftime("%m")
    comment = {
        "memory_id": id,
        "comment_text": request.form.get("comment"),
        "comment_date": month + "-" + year,
        "created_by": session["user"]
    }
    mongo.db.comments.insert_one(comment)
    flash("Comment Successfully Added")

    page, per_page, offset = get_page_args(
    page_parameter='page', per_page_parameter='per_page',
    offset_parameter='offset')

    per_page = 6
    offset = (page - 1) * 6

    memory = mongo.db.memories.find_one({"_id": ObjectId(id)})

    comments = mongo.db.comments.find({"memory_id":  id})
    total_comments = mongo.db.comments.find({"memory_id":  id}).count()
    comments_paginated = comments[offset: offset + per_page]

    pagination = Pagination(page=page, per_page=per_page,
                            total=total_comments, css_framework='bootstrap')

    return render_template("memory.html", memory=memory, comments=comments_paginated, page=page,
                           per_page=per_page,
                           pagination=pagination)

@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    memories = list(mongo.db.memories.find({"$text": {"$search": query}}))
    return render_template("memories.html", memories=memories)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# 404 error page
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', error=error), 404

# 500 error page
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', error=error), 500

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)