from flask import (render_template, Blueprint)

from football_memories import app
errors = Blueprint('errors', __name__)


@app.errorhandler(404)
def error_404(error):
    """
    Render the 404.html template in the case of a 404 error
    """
    return render_template('errors/404.html', error=error), 404


@app.errorhandler(500)
def error_500(error):
    """
    Render the 500.html template in the case of a 500 error
    """
    return render_template('errors/500.html', error=error), 500


@app.errorhandler(400)
def error_400(error):
    """
    Render the 400.html template in the case of a 500 error
    """
    return render_template('errors/400.html', error=error), 400


@app.errorhandler(401)
def error_401(error):
    """
    Render the 401.html template in the case of a 401 error
    """
    return render_template('errors/401.html', error=error), 401


@app.errorhandler(405)
def error_405(error):
    """
    Render the 405.html template in the case of a 405 error
    """
    return render_template('errors/405.html', error=error), 405
