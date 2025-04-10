from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Artist

artists_bp = Blueprint('artists', __name__)

@artists_bp.route('/artists')
@login_required
def list_artists():
    artists = Artist.query.all()
    return render_template('artists/list.html', artists=artists)

@artists_bp.route('/artist/<int:artist_id>')
@login_required
def view_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    return render_template('artists/view.html', artist=artist)