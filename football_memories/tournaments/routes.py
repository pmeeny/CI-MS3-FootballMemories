import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, Blueprint, session,abort)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import current_app
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError
from flask_paginate import Pagination, get_page_args
from football_memories import mongo

if os.path.exists("env.py"):
    import env

client = boto3.client('s3', aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))
tournaments = Blueprint('tournaments', __name__)

@tournaments.route("/get_tournaments")
def get_tournaments():

    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page',
        offset_parameter='offset')

    per_page = 3
    offset = (page - 1) * 3

    username = session["user"]
    user = mongo.db.users.find_one({"username": username})

    total_tournaments = mongo.db.tournaments.find().count()
    tournaments = list(mongo.db.tournaments.find().sort("tournament_name", 1))
    tournaments_paginated = tournaments[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_tournaments, css_framework='bootstrap')

    return render_template("tournaments/tournament.html", tournaments=tournaments_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination, user=user)
    
@tournaments.route("/add_tournament", methods=["GET", "POST"])
def add_tournament():

    if request.method == "POST":
        image = request.files['tournament_image']
        image_file = secure_filename(image.filename)
        image.save(image_file)
        now = datetime.now()
        timestamp=now.strftime("%Y_%m_%d_%H_%M_%S_")
        image_to_upload = timestamp + image_file
        client.upload_file(image_file, 'ci-ms3-football-memories', image_to_upload)
        image_url = "https://ci-ms3-football-memories.s3.eu-west-1.amazonaws.com/" + image_to_upload

        tournament = {
            "tournament_name": request.form.get("tournament_name"),
            "tournament_image": image_url
        }
        mongo.db.tournaments.insert_one(tournament)
        flash("New tournament Added")
        return redirect(url_for("tournaments.get_tournaments"))

    return render_template("tournaments/add_tournament.html")

@tournaments.route("/edit_tournament/<tournament_id>", methods=["GET", "POST"])
def edit_tournament(tournament_id):
    if request.method == "POST":
        image = request.files['tournament_image']
        image_file = secure_filename(image.filename)
        image.save(image_file)
        now = datetime.now()
        timestamp=now.strftime("%Y_%m_%d_%H_%M_%S_")
        image_to_upload = timestamp + image_file
        client.upload_file(image_file, 'ci-ms3-football-memories', image_to_upload)
        image_url = "https://ci-ms3-football-memories.s3.eu-west-1.amazonaws.com/" + image_to_upload

        submit = {
            "tournament_name": request.form.get("tournament_name"),
            "tournament_image": image_url
        }
        mongo.db.tournaments.update({"_id": ObjectId(tournament_id)}, submit)
        flash("Tournament Successfully Updated")
        return redirect(url_for("tournaments.get_tournaments"))

    tournament = mongo.db.tournaments.find_one({"_id": ObjectId(tournament_id)})
    return render_template("tournaments/edit_tournament.html", tournament=tournament)

@tournaments.route("/delete_tournament/<tournament_id>")
def delete_tournament(tournament_id):
    mongo.db.tournaments.remove({"_id": ObjectId(tournament_id)})
    flash("Tournament Successfully Deleted")
    return redirect(url_for("tournaments.get_tournaments"))