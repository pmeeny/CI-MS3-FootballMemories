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
