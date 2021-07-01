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

@administration.route("/terms_and_conditions")
def terms_and_conditions():
    return render_template("administration/terms_and_conditions.html")

@administration.route("/privacy_policy")
def privacy_policy():
       return render_template("administration/privacy_policy.html")

@administration.route("/dashboard")
def dashboard():
    return render_template("administration/dashboard.html")
