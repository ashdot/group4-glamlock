from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user
from models.models import ProductRecommendation, Booking, Product

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations')
@login_required
def view_recommendations():
    if not current_user.client_profile:
        return redirect(url_for('home'))
    
    # Get unique products from artists the client has booked
    client_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    artist_ids = {b.artist_id for b in client_bookings}
    
    # Add distinct() to avoid duplicates
    recommended_products = Product.query.filter(
        Product.artist_id.in_(artist_ids)
    ).distinct(Product.id).all()  # For PostgreSQL
    
    # For SQLite use:
    # recommended_products = list({p.id: p for p in Product.query.filter(
    #     Product.artist_id.in_(artist_ids)
    # ).all().values())
    
    return render_template('recommendations/view.html', 
                         products=recommended_products)