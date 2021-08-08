from flask import (flash, render_template,
                   redirect, request, session, url_for, Blueprint)
from werkzeug.security import generate_password_hash, check_password_hash
from football_memories import mongo

# Create an authentication object as a blueprint
authentication = Blueprint('authentication', __name__)


@authentication.route("/register", methods=["GET", "POST"])
def register() -> object:
    """
    This function registers a new user(and their relevant information)
    in the users collection and once successful brings the user to
    their memories page and a login session is created for the user.
    The users password is stored encrypted
    If the username already exists, the user is redirected back
    to the register page
    :return render_template of get_memories
    """
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # If the user already exists, redirect them to the register page
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
        try:
            # Insert the register object in the users collection
            mongo.db.users.insert_one(register)
            # Insert the new user into 'session' cookie
            session["user"] = request.form.get("username").lower()
            flash("Registration Successful!")
        except Exception as e:
            flash("An exception occurred when adding a new user: " +
                  getattr(e, 'message', repr(e)))
        return redirect(url_for("memories.get_memories",
                                username=session["user"]))
    return render_template("authentication/register.html")


@authentication.route("/login", methods=["GET", "POST"])
def login() -> object:
    """
    This function, checks the user exists and successfully logs
    in the user and redirects them to their memories page.
    If the user submits and incorrect username and/or password
    they are redirected to the login page
    :return render_template of get_memories
    """
    if request.method == "POST":
        # Check if the username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            # Ensure the hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                # Redirect to users memories page
                return redirect(url_for(
                    "memories.get_memories",
                    username=session["user"]))
            else:
                # Invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("authentication.login"))
        else:
            # Username doesn't exist in the users collection
            flash("Incorrect Username and/or Password")
            return redirect(url_for("authentication.login"))
    return render_template("authentication/login.html")


@authentication.route("/logout")
def logout() -> object:
    """
    This function logs the user out of the site, removes this
    session and redirects them to the home/landing page
    :return render_template of administration.home
    """
    # Remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("administration.home"))


@authentication.route("/profile/<username>", methods=["GET"])
def profile(username: object) -> object:
    """
    This function renders the profile page and displays
    the users profile information once the user is logged in
    and exists in the users collection
    :param username: username of user
    :return render_template of profile.html
    """
    # If the user is not logged in, redirect them to home/landing page
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    # Find the user in the users collection
    user = mongo.db.users.find_one({"username": username})
    return render_template("authentication/profile.html",
                           username=session['user'], user=user)


@authentication.route("/update_profile/<username>", methods=["GET", "POST"])
def update_profile(username: object) -> object:
    """
    This function updates the users profile with the updated information
    they have submitted
    :param username: username of user
    :return render_template of profile.html
    """
    # Create an update_profile object with the updated information
    if request.method == "POST":
        # Get the user and their user_type, regular_user or admin_user
        user = mongo.db.users.find_one({"username": username})
        user_type = user['user_type']
        # Create an object update_profile with the updated information
        update_profile = {
            "user_type": user_type,
            "username": session['user'],
            "password": generate_password_hash(request.form.get("password")),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "favourite_team": request.form.get("favourite_team"),
            "country": request.form.get("country")
        }
        try:
            # Update the users information in the users collection
            mongo.db.users.update({"username": username}, update_profile)
            flash("User Profile Successfully Updated")
        except Exception as e:
            flash("An exception occurred when updating the user: " +
                  getattr(e, 'message', repr(e)))
    # Search for the user and redirect them back to their profile page
    # with their updated information displayed
    user = mongo.db.users.find_one({"username": username})
    return render_template("authentication/profile.html",
                           username=session['user'], user=user)


@authentication.route("/delete_profile/<username>")
def delete_profile(username: object) -> object:
    """
    This function deletes all information linked to a user and their username
    It deletes all memories added by the user, and the comments/ratings linked
    to the memories from the memories, ratings, comments collections
    It deletes all comments added by the user on other users memories from
    the comments collection
    It deletes all ratings added by the user on other users memories from
    the ratings collection
    Finally it deletes the user from the users collection and redirects the
    user to the home/landing page
    :param username: username of user
    :return redirect to administration.home
    """
    # For each memory, created by a user, get the memory_id, and delete
    # and comments/ratings with that memory_id in the comments and ratings
    # collections
    try:
        memories_to_delete = list(mongo.db.memories.find(
                                {"memory_created_by": username}))
        for memory in memories_to_delete:
            memory_id = str(memory['_id'])
            mongo.db.comments.delete_many({"memory_id": memory_id})
            mongo.db.ratings.delete_many({"memory_id": memory_id})
        # Delete any memories created by the user in the memories collection
        mongo.db.memories.delete_many({"memory_created_by": username})
        # Delete all comments by user: comments.comment_created_by
        mongo.db.comments.remove({"comment_created_by": username})
        # delete all ratings by user: ratings.rating_created_by
        mongo.db.ratings.remove({"rating_created_by": username})
        # Delete user from users collection, where the username matches
        mongo.db.users.remove({"username": username})
        # Redirect user to homepage/landing page
        flash("Your account has been deleted and you have been logged out")
        session.pop("user")
    except Exception as e:
        flash("An exception occurred when deleting the user: " +
              getattr(e, 'message', repr(e)))
    return redirect(url_for("administration.home"))
