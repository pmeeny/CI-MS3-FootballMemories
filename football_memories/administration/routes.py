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


administration = Blueprint('administration', __name__)


@administration.route("/")
@administration.route("/home")
def home():
    three_latest_memories = list(mongo.db.memories.find().sort("_id", -1).limit(3))
    print ("latest memories")
    print (three_latest_memories)
    return render_template("administration/index.html", memories=three_latest_memories)    

@administration.route("/terms_and_conditions")
def terms_and_conditions():
    return render_template("administration/terms_and_conditions.html")

@administration.route("/privacy_policy")
def privacy_policy():
       return render_template("administration/privacy_policy.html")

@administration.route("/dashboard")
def dashboard():
    number_of_users = mongo.db.users.count()
    number_of_memories = mongo.db.memories.count()
    number_of_comments = mongo.db.comments.count()
    return render_template("administration/dashboard.html",
        number_of_users=number_of_users, 
        number_of_memories=number_of_memories, 
        number_of_comments=number_of_comments)
