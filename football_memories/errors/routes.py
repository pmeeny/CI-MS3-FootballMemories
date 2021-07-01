from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, Blueprint, session,abort)

from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import current_app

from flask_paginate import Pagination, get_page_args

from football_memories import mongo

errors = Blueprint('errors', __name__)

# 404 error page
@errors.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', error=error), 404

# 500 error page
@errors.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', error=error), 500