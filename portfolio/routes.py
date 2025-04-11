from flask import Blueprint, abort, current_app, render_template, redirect, url_for, flash
from flask_login import login_required, current_user


portfolio_bp = Blueprint('portfolio', __name__)


@portfolio_bp.route('/create_portfolio', methods =['GET','POST'])
@login_required
def artist_portfolio():
    if not hasattr(current_user, 'artist_profile'):
        abort(403)
    

    
    

    
    return render_template('portfolio/create_portfolio.html')