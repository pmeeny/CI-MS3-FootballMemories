from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, Blueprint, session,abort)

from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from flask import current_app

from flask_paginate import Pagination, get_page_args

from football_memories import mongo

memories = Blueprint('memories', __name__)

@memories.route("/get_memories")
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

    return render_template("memories/memories.html", memories=memories_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@memories.route("/get_memory/<id>")
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

    return render_template("memories/memory.html", memory=memory, comments=comments_paginated, page=page,
                           per_page=per_page,
                           pagination=pagination)

@memories.route("/get_user_memories")
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

    return render_template("memories/memories.html", memories=user_memories_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)

@memories.route("/add_memory", methods=["GET", "POST"])
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
    return render_template("memories/add_memory.html", tournaments=tournaments)

@memories.route("/edit_memory/<memory_id>", methods=["GET", "POST"])
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
    return render_template("memories/edit_memory.html", memory=memory, tournaments=tournaments)

@memories.route("/delete_memory/<memory_id>")
def delete_memory(memory_id):

    mongo.db.memories.remove({"_id": ObjectId(memory_id)})
    flash("Memory Successfully Deleted")
    return redirect(url_for("get_memories"))

@memories.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    memories = list(mongo.db.memories.find({"$text": {"$search": query}}))
    return render_template("memories/memories.html", memories=memories)

@memories.route("/add_comment/<id>", methods=["POST"])
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

    return render_template("memories/memory.html", memory=memory, comments=comments_paginated, page=page,
                           per_page=per_page,
                           pagination=pagination)


    query = request.form.get("query")
    memories = list(mongo.db.memories.find({"$text": {"$search": query}}))
    return render_template("memories/memories.html", memories=memories)