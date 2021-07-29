from flask import (flash, render_template,
                   redirect, request, url_for, Blueprint, session)
from bson.objectid import ObjectId
from flask_paginate import Pagination
from football_memories import mongo
from football_memories.util import util

# Create a memories object as a blueprint
memories = Blueprint('memories', __name__)


@memories.route("/get_memories")
def get_memories():
    """
    This function renders the memories template to display all memories for
    all users and displays pagination if the amount is greater than three memories
    """
    # Check the user is logged in
    if 'user' not in session:
        return redirect(url_for("administration.home"))

    offset, per_page, page = util.setupPagination()

    # Get the users details
    username = session["user"]
    user = mongo.db.users.find_one({"username": username})

    # Get all memories and the memory count
    total_memories = mongo.db.memories.find().count()
    memories_sorted_by = mongo.db.memories.find().sort("memory_created_by", 1)
    memories_paginated = memories_sorted_by[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_memories, css_framework='bootstrap')

    # Render the memories template with the relevant parameters
    return render_template("memories/memories.html",
                           memories=memories_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination, user=user,
                           selected="get_memories")


@memories.route("/get_memory/<id>")
def get_memory(id):
    """
    This function renders the memory template to display memory information
    for a selected memory.
    """
    # Check the user is logged in
    if 'user' not in session:
        return redirect(url_for("administration.home"))

    # Get the average rating for the selected memory
    round_av_rating = calculateAverageRating(id)

    offset, per_page, page = util.setupPagination()

    # Get the memory information and associated comments
    memory = mongo.db.memories.find_one({"_id": ObjectId(id)})
    comments = mongo.db.comments.find({"memory_id": id}).sort("_id", -1)
    total_comments = mongo.db.comments.find({"memory_id": id}).count()

    # Get the current view count of the memory, and increment
    view_count = memory['memory_view_count']
    new_view_count = view_count + 1

    # Update the memory view count in the database
    mongo.db.memories.update({"_id": ObjectId(id)},
                             {"$set": {"memory_view_count": new_view_count}})

    # Setup pagination for the comments
    comments_paginated = comments[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_comments, css_framework='bootstrap')

    # Render the memory template with the relevant parameters
    return render_template("memories/memory.html", memory=memory,
                           comments=comments_paginated, page=page,
                           per_page=per_page,
                           pagination=pagination,
                           average_rating=round_av_rating)


@memories.route("/get_user_memories")
def get_user_memories():
    """
    This function returns all memories added by a specific user
    """
    # Check the user is logged in
    if 'user' not in session:
        return redirect(url_for("administration.home"))

    # Setup pagination and get the user information
    offset, per_page, page = util.setupPagination()
    username = session["user"]

    # Get the memories for the specific user
    total_user_memories = mongo.db.memories.find(
        {"memory_created_by": username}).count()
    user_memories = mongo.db.memories.find({"memory_created_by": username})
    user_memories_paginated = user_memories[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total_user_memories,
                            css_framework='bootstrap')

    # Render the memories template with the relevant parameters
    return render_template("memories/memories.html",
                           memories=user_memories_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           selected="get_user_memories")


@memories.route("/add_memory", methods=["GET", "POST"])
def add_memory():
    """
    This function adds a memory with the information passed down
    from the add memory template
    """
    # Check the user is logged in
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    
    if request.method == "POST": 
        # Check if the file type is an allowed image file type
        memory_image_type, allowedImageFileTypes = util.isAllowedImageFileType('tournament_image')
        
        if (memory_image_type) not in allowedImageFileTypes:
            flash("File type " + memory_image_type + " not allowed, allowed file types are: jpg, JPG ,png ,PNG")
            return redirect(url_for("memories.get_user_memories"))
        
        image_url = util.storeImageAWSS3Bucket('memory_image')      

    if request.method == "POST":
        # Store the memory image in an S3 bucket
        image_url = util.storeImageAWSS3Bucket('memory_image')

        # Create a memory object with the memory information
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
        # Create the memory in the memories collection in the mongodb
        mongo.db.memories.insert_one(memory)
        flash("Memory Successfully Added")
        # Redirect to the get_user_memories route
        return redirect(url_for("memories.get_user_memories"))

    tournaments = mongo.db.tournaments.find().sort("tournament_name", 1)
    return render_template("memories/add_memory.html",
                           tournaments=tournaments)


@memories.route("/edit_memory/<memory_id>", methods=["GET", "POST"])
def edit_memory(memory_id):
    """
    This function edits a memory with the information passed down
    from the edit memory template
    """
    # Check the user is logged in
    if 'user' not in session:
        return redirect(url_for("administration.home"))
    
    if request.method == "POST":
        # Check if the file type is an allowed image file type
        memory_image_type, allowedImageFileTypes = util.isAllowedImageFileType('tournament_image')
        
        if (memory_image_type) not in allowedImageFileTypes:
            flash("File type " + memory_image_type + " not allowed, allowed file types are: jpg, JPG ,png ,PNG")
            return redirect(url_for("memories.get_user_memories"))
        
        image_url = util.storeImageAWSS3Bucket('memory_image')     

        # Create a memory_to_update object with the new memory information
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
        # Update the memory in the memories collection in the mongodb
        mongo.db.memories.update({"_id": ObjectId(memory_id)},
                                 memory_to_update)
        flash("Memory Successfully Updated")
        # Redirect to the get_user_memories route
        return redirect(url_for("memories.get_user_memories"))

    memory = mongo.db.memories.find_one({"_id": ObjectId(memory_id)})
    tournaments = mongo.db.tournaments.find().sort("tournament_name", 1)
    return render_template("memories/edit_memory.html",
                           memory=memory,
                           tournaments=tournaments)


@memories.route("/delete_memory/<memory_id>")
def delete_memory(memory_id):
    """
    This function deletes a memory and all associated comment and ratings
    """
    mongo.db.memories.remove({"_id": ObjectId(memory_id)})
    mongo.db.comments.remove({"memory_id": memory_id})
    mongo.db.ratings.remove({"memory_id": memory_id})
    flash("Memory Successfully Deleted")
    return redirect(url_for("memories.get_user_memories"))


@memories.route("/search", methods=["GET", "POST"])
def search():
    """
    This function allows the user to search memories based on a search criteria
    The memory_name and memory_description have search indexes setup for search
    """
    offset, per_page, page = util.setupPagination()

    # Get the users information
    username = session["user"]
    user = mongo.db.users.find_one({"username": username})

    # Create a query based on what the suer has entered as search criteria
    query = request.form.get("query")
    # Search in the memories collection for the search query text
    memories = list(mongo.db.memories.find(
        {"$text": {"$search": query}}))
    memories_count = mongo.db.memories.find(
        {"$text": {"$search": query}}).count()

    # Setup pagination to display the memory search information
    memories_paginated = memories[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=memories_count, css_framework='bootstrap')
    # Render the memories template with the updated information
    return render_template("memories/memories.html",
                           memories=memories_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination, user=user)


@memories.route("/add_comment/<id>", methods=["POST"])
def add_comment(id):
    """
    This function adds a comment for a particular memory id
    """
    # Check the user is logged in
    if 'user' not in session:
        return redirect(url_for("administration.home"))

    # Get the current month and year
    month, year = util.getMonthAndYear()
    # Create a comment object
    comment = {
        "memory_id": id,
        "comment_text": request.form.get("comment"),
        "comment_date": month + "-" + year,
        "comment_created_by": session["user"]
    }
    # Create a comment in the comments collection with the comment object
    mongo.db.comments.insert_one(comment)
    flash("Comment Successfully Added")
    # Redirect to the specific memory that the comment was added to
    return redirect(url_for("memories.get_memory", id=id))


@memories.route("/add_rating/<id>", methods=["POST"])
def add_rating(id):
    """
    This function adds a rating(from 1 to 5) for a particular memory id
    """
    # Check the user is logged in
    if 'user' not in session:
        return redirect(url_for("administration.home"))

    # Create a rating object
    rating = {
        "memory_id": id,
        "rating_value": int(request.form.get("rating")),
        "rating_created_by": session["user"]
    }

    # Create a rating in the ratings collection in the mongodb
    mongo.db.ratings.insert_one(rating)
    flash("Rating Successfully Added")
    # Redirect to the specific memory that the rating was added to
    return redirect(url_for("memories.get_memory", id=id))


def calculateAverageRating(id):
    """
    This function
    """
    # Get all ratings for a memory id
    ratings = mongo.db.ratings.find({"memory_id": id})
    round_av_rating = 0
    total = 0
    i = 0

    # Get the sum of all ratings for a memory id
    for rating in ratings:
        i = i + 1
        total = total + rating.get("rating_value")

    # Get the average rating based on the number of ratings
    if i > 0:
        av_rating = total / i
        round_av_rating = (round((av_rating), 2))
    # Return the average rating to one decimal point
    return round_av_rating
