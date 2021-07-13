from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, Blueprint, session, abort)
from flask import current_app

errors = Blueprint('errors', __name__)


@errors.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', error=error), 404


@errors.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', error=error), 500
