import os
import boto3
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, Blueprint, session, abort)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import current_app
from botocore.exceptions import NoCredentialsError
from flask_paginate import Pagination, get_page_args
from football_memories import mongo
if os.path.exists("env.py"):
    import env

s3_bucket_name = "ci-ms3-football-memories"
s3_bucket_url = "https://ci-ms3-football-memories.s3.eu-west-1.amazonaws.com/"
client = boto3.client('s3', 
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))
memories = Blueprint('memories', __name__)


@memories.route("/get_memories")
def get_memories():
    """
    TBC
    """
    if 'user' not in session:
        return redirect(url_for("administration.home"))    

    offset, per_page, page = setupPagination()

    username = session["user"]
    user = mongo.db.users.find_one({"username": username})

    total_memories = mongo.db.memories.find().count()
    memories = mongo.db.memories.find().sort("memory_created_by", 1)
    memories_paginated = memories[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_memories, css_framework='bootstrap')

    return render_template("memories/memories.html",
                           memories=memories_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination, user=user,
                           selected="get_memories")


@memories.route("/get_memory/<id>")
def get_memory(id):
    """
    TBC
    """
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    
    round_av_rating = calculateAverageRating(id)

    offset, per_page, page = setupPagination()

    memory = mongo.db.memories.find_one({"_id": ObjectId(id)})

    comments = mongo.db.comments.find({"memory_id":  id}).sort("_id", -1)
    total_comments = mongo.db.comments.find({"memory_id":  id}).count()

    view_count = memory['memory_view_count']
    view_count1 = view_count+1

    mongo.db.memories.update({"_id": ObjectId(id)},
                             {"$set": {"memory_view_count": view_count1}})

    comments_paginated = comments[offset: offset + per_page]

    pagination = Pagination(page=page, per_page=per_page,
                            total=total_comments, css_framework='bootstrap')

    return render_template("memories/memory.html", memory=memory,
                           comments=comments_paginated, page=page,
                           per_page=per_page,
                           pagination=pagination,
                           average_rating=round_av_rating)


@memories.route("/get_user_memories")
def get_user_memories():
    """
    TBC
    """
    if 'user' not in session:
        return redirect(url_for("administration.home"))
        
    offset, per_page, page = setupPagination()

    username = session["user"]

    total_user_memories = mongo.db.memories.find(
                        {"memory_created_by": username}).count()
    user_memories = mongo.db.memories.find({"memory_created_by": username})
    user_memories_paginated = user_memories[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_user_memories,
                            css_framework='bootstrap')

    return render_template("memories/memories.html",
                           memories=user_memories_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           selected="get_user_memories")


@memories.route("/add_memory", methods=["GET", "POST"])
def add_memory():
    """
    TBC
    """
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    
    if request.method == "POST":
        image = request.files['memory_image']
        image_file = secure_filename(image.filename)
        image.save(image_file)
        now = datetime.now()
        timestamp = now.strftime("%Y_%m_%d_%H_%M_%S_")
        image_to_upload = timestamp + image_file

        client.upload_file(image_file, 'ci-ms3-football-memories',
                           image_to_upload)

        image_url = s3_bucket_url + image_to_upload

        memory = {
            "memory_image": image_url,
            "tournament_name": request.form.get("tournament_name"),
            "memory_name": request.form.get("memory_name"),
            "memory_description": request.form.get("memory_description"),
            "memory_date": request.form.get("memory_date"),
            "memory_stadium": request.form.get("memory_stadium"),
            "memory_view_count": (0),
            "memory_created_by": session["user"]
        }
        mongo.db.memories.insert_one(memory)
        flash("Memory Successfully Added")
        return redirect(url_for("memories.get_memories"))

    tournaments = mongo.db.tournaments.find().sort("tournament_name", 1)
    return render_template("memories/add_memory.html",
                           tournaments=tournaments)


@memories.route("/edit_memory/<memory_id>", methods=["GET", "POST"])
def edit_memory(memory_id):
    """
    TBC
    """
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    if request.method == "POST":
        image_url = storeImageAWSS3Bucket()

        memory_to_update = {
            "memory_image": image_url,
            "tournament_name": request.form.get("tournament_name"),
            "memory_name": request.form.get("memory_name"),
            "memory_description": request.form.get("memory_description"),
            "memory_date": request.form.get("memory_date"),
            "memory_stadium": request.form.get("memory_stadium"),
            "memory_created_by": session["user"],
            "memory_view_count": (0)
        }
        mongo.db.memories.update({"_id": ObjectId(memory_id)},
                                 memory_to_update)
        flash("Memory Successfully Updated")
        return redirect(url_for("memories.get_user_memories"))

    memory = mongo.db.memories.find_one({"_id": ObjectId(memory_id)})
    tournaments = mongo.db.tournaments.find().sort("tournament_name", 1)
    return render_template("memories/edit_memory.html",
                           memory=memory,
                           tournaments=tournaments)


@memories.route("/delete_memory/<memory_id>")
def delete_memory(memory_id):
    """
    TBC
    """
    mongo.db.memories.remove({"_id": ObjectId(memory_id)})
    mongo.db.comments.remove({"memory_id": memory_id})
    mongo.db.ratings.remove({"memory_id": memory_id})
    flash("Memory Successfully Deleted")
    return redirect(url_for("memories.get_memories"))


@memories.route("/search", methods=["GET", "POST"])
def search():
    """
    TBC
    """
    offset, per_page, page = setupPagination()

    username = session["user"]
    user = mongo.db.users.find_one({"username": username})

    query = request.form.get("query")
    memories = list(mongo.db.memories.find(
                            {"$text": {"$search": query}}))
    memories_count = mongo.db.memories.find(
                            {"$text": {"$search": query}}).count()

    memories_paginated = memories[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=memories_count, css_framework='bootstrap')
    return render_template("memories/memories.html",
                           memories=memories_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination, user=user)


@memories.route("/add_comment/<id>", methods=["POST"])
def add_comment(id):
    """
    TBC
    """
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    
    month, year = getMonthAndYear()
    comment = {
        "memory_id": id,
        "comment_text": request.form.get("comment"),
        "comment_date": month + "-" + year,
        "comment_created_by": session["user"]
    }
    mongo.db.comments.insert_one(comment)
    flash("Comment Successfully Added")
    return redirect(url_for("memories.get_memory", id=id))


@memories.route("/add_rating/<id>", methods=["POST"])
def add_rating(id):
    """
    TBC
    """
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    
    rating = {
        "memory_id": id,
        "rating_value": int(request.form.get("rating")),
        "rating_created_by": session["user"]
    }

    mongo.db.ratings.insert_one(rating)
    flash("Rating Successfully Added")
    return redirect(url_for("memories.get_memory", id=id))


def setupPagination():
    """
    TBC
    """
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page',
        offset_parameter='offset')

    per_page = 3
    offset = (page - 1) * 3
    return offset, per_page, page


def getMonthAndYear():
    """
    TBC
    """
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    return month, year


def storeImageAWSS3Bucket():
    """
    TBC
    """
    image = request.files['memory_image']
    image_file = secure_filename(image.filename)
    image.save(image_file)
    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d_%H_%M_%S_")
    image_to_upload = timestamp + image_file
    client.upload_file(image_file, s3_bucket_name, image_to_upload)
    image_url = s3_bucket_url + image_to_upload
    return image_url


def calculateAverageRating(id):
    """
    TBC
    """
    ratings = mongo.db.ratings.find({"memory_id":  id})
    round_av_rating = 0
    total = 0
    i = 0

    for rating in ratings:
        i = i+1
        total = total + rating.get("rating_value")

    if i > 0:
        av_rating = total/i
        round_av_rating = (round((av_rating), 2))
    return round_av_rating
