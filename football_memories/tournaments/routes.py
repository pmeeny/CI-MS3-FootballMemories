import os
from flask import (flash, render_template,
    redirect, request, url_for, Blueprint, session, abort)
from bson.objectid import ObjectId
from datetime import datetime
from flask_paginate import Pagination, get_page_args
from football_memories import mongo
from football_memories.util import util

if os.path.exists("env.py"):
    import env

tournaments = Blueprint('tournaments', __name__)


@tournaments.route("/get_tournaments")
def get_tournaments():
    """
    TBC
    """
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    
    offset, per_page, page = util.setupPagination()
    username = session["user"]
    user = mongo.db.users.find_one({"username": username})

    total_tournaments = mongo.db.tournaments.find().count()
    tournaments = list(mongo.db.tournaments.find().sort("tournament_name", 1))
    tournaments_paginated = tournaments[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_tournaments, css_framework='bootstrap')

    return render_template("tournaments/tournament.html",
                           tournaments=tournaments_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination, user=user)


@tournaments.route("/add_tournament", methods=["GET", "POST"])
def add_tournament():
    """
    TBC
    """
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    
    if request.method == "POST":
        # check if tournament name already exists in db
        existing_tournament = mongo.db.tournaments.find_one(
            {"tournament_name": request.form.get("tournament_name")})

        if existing_tournament:
            flash("Tournament name already exists")
            return redirect(url_for("tournaments.get_tournaments"))
        
        image_url = util.storeImageAWSS3Bucket('tournament_image')

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
    """
    TBC
    """
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    
    if request.method == "POST":
        # check if tournament name already exists in db
        existing_tournament = mongo.db.tournaments.find_one(
            {"tournament_name": request.form.get("tournament_name")})

        if existing_tournament:
            flash("Tournament name already exists")
            return redirect(url_for("tournaments.get_tournaments"))
        
        image_url = util.storeImageAWSS3Bucket('tournament_image')

        submit = {
            "tournament_name": request.form.get("tournament_name"),
            "tournament_image": image_url
        }
        mongo.db.tournaments.update({"_id": ObjectId(tournament_id)},
                                    submit)
        flash("Tournament Successfully Updated")
        return redirect(url_for("tournaments.get_tournaments"))

    tournament = mongo.db.tournaments.find_one(
                    {"_id": ObjectId(tournament_id)})
    return render_template("tournaments/edit_tournament.html",
                           tournament=tournament)


@tournaments.route("/delete_tournament/<tournament_id>",
                   methods=["GET", "POST"])
def delete_tournament(tournament_id):
    """
    TBC
    """
    tournament = mongo.db.tournaments.find_one(
               {"_id": ObjectId(tournament_id)})
    number_of_memories = mongo.db.memories.find(
                {"tournament_name": tournament['tournament_name']}).count()

    if(number_of_memories > 0):
        flash("A tournament than contains memories cannot be deleted")
    else:
        # Get the count of tournaments in the tournament collection
        number_of_tournaments = mongo.db.tournaments.find().count()
        if(number_of_tournaments == 1):
            flash("Cannot delete this tournament as a minimum of one tournament is required")
        else:
            mongo.db.tournaments.remove({"_id": ObjectId(tournament_id)})
            flash("Tournament Successfully Deleted")

    return redirect(url_for("tournaments.get_tournaments"))
