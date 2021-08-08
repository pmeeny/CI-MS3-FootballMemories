from bson.objectid import ObjectId
from flask import (flash, render_template,
                   redirect, request, url_for, Blueprint, session)
from flask_paginate import Pagination
from football_memories import mongo
from football_memories.util import util

# Create a tournaments object as a blueprint
tournaments = Blueprint('tournaments', __name__)


@tournaments.route("/get_tournaments")
def get_tournaments() -> object:
    """
    This function renders the tournament template with all tournaments
    in the tournament collection, the most recent added is displayed first
    :return render_template of tournament.html
    """
    # Check the user is logged in
    if 'user' not in session:
        return redirect(url_for("administration.home"))

    # Setup pagination
    offset, per_page, page = util.setup_pagination()

    # Get the user information
    username = session["user"]
    user = mongo.db.users.find_one({"username": username})

    # Get the tournament information and count
    total_tournaments = mongo.db.tournaments.find().count()
    tournaments = list(mongo.db.tournaments.find().sort("_id", -1))
    tournaments_paginated = tournaments[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_tournaments, css_framework='bootstrap')

    # Render the tournament template with the relevant tournament information
    return render_template("tournaments/tournament.html",
                           tournaments=tournaments_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination, user=user)


@tournaments.route("/add_tournament", methods=["GET", "POST"])
def add_tournament() -> object:
    """
    This function adds a tournament with tournament name and image
    :return redirect to get_tournaments
    """
    # Check the user is logged in
    if 'user' not in session:
        return redirect(url_for("administration.home"))

    if request.method == "POST":

        # Check if the file type is an allowed image file type
        tournament_image_type, allowed_image_file_types = \
            util.is_image_type_allowed('tournament_image')

        if tournament_image_type not in allowed_image_file_types:
            flash("File type " + tournament_image_type +
                  " not allowed," +
                  " allowed file types are: jpg, JPG ,png ,PNG")
            return redirect(url_for("tournaments.get_tournaments"))

        # Check if the tournament name already exists in db
        existing_tournament = mongo.db.tournaments.find_one(
            {"tournament_name": request.form.get("tournament_name")})

        # Display a message to the user and redirect to tournaments page
        if existing_tournament:
            flash("Tournament name already exists")
            return redirect(url_for("tournaments.get_tournaments"))
        try:
            # Store the tournament image in the AWS S3 bucket
            image_url = util.store_image_in_aws_s3_bucket('tournament_image')

            # Create a tournament object with a name and image
            tournament = {
                "tournament_name":
                    request.form.get("tournament_name"),
                "tournament_image": image_url
            }
            # Create the tournament in the tournaments collection
            # in mongodb
            mongo.db.tournaments.insert_one(tournament)
            flash("New tournament Added")
        except Exception as e:
            flash("An exception occurred when adding a new tournament: " +
                  getattr(e, 'message', repr(e)))
        # Redirect the user to the get tournaments route
        return redirect(url_for("tournaments.get_tournaments"))

    return render_template("tournaments/add_tournament.html")


@tournaments.route("/edit_tournament/<tournament_id>", methods=["GET", "POST"])
def edit_tournament(tournament_id: object) -> object:
    """
    This function edits a tournament with updated tournament name and image
    :param tournament_id: Identifier of tournament
    :return redirect to get_tournaments
    """
    # Check the user is logged in
    if 'user' not in session:
        return redirect(url_for("administration.home"))

    if request.method == "POST":
        # Check if the file type is an allowed image file type
        tournament_image_type, allowed_image_file_types = \
            util.is_image_type_allowed('tournament_image')

        if tournament_image_type not in allowed_image_file_types:
            flash("File type " + tournament_image_type +
                  " not allowed, " +
                  "allowed file types are: jpg, JPG ,png ,PNG")
            return redirect(url_for("tournaments.get_tournaments"))

        # Check if tournament name already exists in db
        existing_tournament = mongo.db.tournaments.find_one(
            {"tournament_name": request.form.get("tournament_name")})

        if existing_tournament:
            flash("Tournament name already exists")
            return redirect(url_for("tournaments.get_tournaments"))

        try:
            # Store the tournament image in the AWS S3 bucket
            image_url = util.store_image_in_aws_s3_bucket('tournament_image')

            # Create a tournament object with a name and image
            updated_tournament = {
                "tournament_name": request.form.get("tournament_name"),
                "tournament_image": image_url
            }
            # Update the tournament in the tournaments collection
            # in the mongodb
            mongo.db.tournaments.update({"_id": ObjectId(tournament_id)},
                                        updated_tournament)
            flash("Tournament Successfully Updated")
        except Exception as e:
            flash("An exception occurred when editing the tournament: " +
                  getattr(e, 'message', repr(e)))
        # Redirect the user to the get tournaments route
        return redirect(url_for("tournaments.get_tournaments"))

    # Return the selected tournament
    tournament = mongo.db.tournaments.find_one(
                    {"_id": ObjectId(tournament_id)})
    return render_template("tournaments/edit_tournament.html",
                           tournament=tournament)


@tournaments.route("/delete_tournament/<tournament_id>",
                   methods=["GET", "POST"])
def delete_tournament(tournament_id: object) -> object:
    """
    This function deletes a tournament
    :param tournament_id: Identifier of tournament
    :return redirect to get_tournaments
    """
    # Get the tournament information
    tournament = mongo.db.tournaments.find_one(
               {"_id": ObjectId(tournament_id)})
    # Get the number of memories within the tournament
    number_of_memories = mongo.db.memories.find(
                {"tournament_name": tournament['tournament_name']}).count()

    # If the tournament has memories if cannot be deleted
    if number_of_memories > 0:
        flash("A tournament than contains memories cannot be deleted")
    else:
        # Get the count of tournaments in the tournament collection
        number_of_tournaments = mongo.db.tournaments.find().count()
        if number_of_tournaments == 1:
            flash("Cannot delete this tournament as a " +
                  "minimum of one tournament is required")
        else:
            # Delete the tournament from the tournaments collection
            try:
                mongo.db.tournaments.remove({"_id": ObjectId(tournament_id)})
                flash("Tournament Successfully Deleted")
            except Exception as e:
                flash("An exception occurred when deleting the tournament: " +
                      getattr(e, 'message', repr(e)))
    # Redirect to the get tournaments page
    return redirect(url_for("tournaments.get_tournaments"))
