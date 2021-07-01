import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, Blueprint, session,abort)

from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import current_app

from flask_paginate import Pagination, get_page_args

from football_memories import mongo

tournaments = Blueprint('tournaments', __name__)

@tournaments.route("/get_tournaments")
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

    return render_template("tournaments/tournament.html", tournaments=tournaments_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)
    
@tournaments.route("/add_tournament", methods=["GET", "POST"])
def add_tournament():
    if request.method == "POST":
        tournament = {
            "tournament_name": request.form.get("tournament_name")
        }
        mongo.db.tournaments.insert_one(tournament)
        flash("New tournament Added")
        return redirect(url_for("tournaments.get_tournaments"))

    return render_template("tournaments/add_tournament.html")

@tournaments.route("/edit_tournament/<tournament_id>", methods=["GET", "POST"])
def edit_tournament(tournament_id):
    if request.method == "POST":
        submit = {
            "tournament_name": request.form.get("tournament_name")
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