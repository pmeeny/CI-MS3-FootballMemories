from flask import (render_template,
                   redirect, url_for, Blueprint, session)
from football_memories import mongo

# Create an administration object as a blueprint
administration = Blueprint('administration', __name__)


@administration.route("/")
@administration.route("/home")
def home() -> object:
    """
    This function displays the last three memories on the index template
    :return render_template of index.html
    """
    # Get the last three memories added to the memories collection
    three_latest_memories = list(mongo.db.memories.find().
                                 sort("_id", -1).limit(3))
    return render_template("administration/index.html",
                           memories=three_latest_memories)


@administration.route("/terms_and_conditions")
def terms_and_conditions() -> object:
    """
    This function renders the terms and conditions template
    :return render_template of terms_and_conditions.html
    """
    return render_template("administration/terms_and_conditions.html")


@administration.route("/privacy_policy")
def privacy_policy() -> object:
    """
    This function renders the privacy policy template
    :return render_template of privacy_policy.html
    """
    return render_template("administration/privacy_policy.html")


@administration.route("/dashboard")
def dashboard() -> object:
    """
    This function renders the dashboard template with information
    from five queries(all counts) of the users, tournaments, memories
    comments and ratings collection
    :return render_template of dashboard.html
    """
    # Check the user is logged in
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    number_of_users = mongo.db.users.count()
    number_of_tournaments = mongo.db.tournaments.count()
    number_of_memories = mongo.db.memories.count()
    number_of_comments = mongo.db.comments.count()
    number_of_ratings = mongo.db.ratings.count()
    return render_template("administration/dashboard.html",
                           number_of_users=number_of_users,
                           number_of_tournaments=number_of_tournaments,
                           number_of_memories=number_of_memories,
                           number_of_comments=number_of_comments,
                           number_of_ratings=number_of_ratings)
