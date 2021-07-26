from flask import (render_template, Blueprint)

errors = Blueprint('errors', __name__)


@errors.errorhandler(404)
def error_404(error):
    """
    Render the 404.html template in the case of a 404 error
    """
    return render_template('errors/404.html', error=error), 404


@errors.errorhandler(500)
def error_500(error):
    """
    Render the 500.html template in the case of a 500 error
    """
    return render_template('errors/500.html', error=error), 500
