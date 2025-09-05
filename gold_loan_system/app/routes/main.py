from flask import render_template, Blueprint
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Public index page."""
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Protected dashboard page, accessible after login."""
    return render_template('dashboard.html', title='Dashboard')
