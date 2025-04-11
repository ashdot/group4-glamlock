from flask import Blueprint, abort, current_app, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.models import Portfolio, PortfolioItem, db
from forms.forms import PortfolioForm, PortfolioItemForm
from utils import allowed_file
import os
import uuid

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/create_portfolio', methods=['GET', 'POST'])
@login_required
def create_portfolio():
    # Check if user has an artist profile
    if not current_user.is_authenticated or not current_user.artist_profile:
        abort(403)
    
    artist = current_user.artist_profile
    if not artist:
        abort(403)
        
    form = PortfolioForm()
    
    if form.validate_on_submit():
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], 
                    unique_filename
                )
                file.save(file_path)
                
                # Create new portfolio or update existing
                if artist.portfolio:
                    portfolio = artist.portfolio
                    action = 'updated'
                else:
                    # Create portfolio without artist parameter
                    portfolio = Portfolio(
                        portfolioName=form.name.data,
                        description=form.description.data,
                        url=unique_filename
                    )
                    portfolio.artist = artist  # Set relationship after creation
                    action = 'created'
                
                portfolio.portfolioName = form.name.data
                portfolio.description = form.description.data
                portfolio.url = unique_filename
                
                db.session.add(portfolio)
                db.session.commit()
                flash(f'Portfolio {action} successfully!', 'success')
                return redirect(url_for('portfolio.view_portfolio'))

        return redirect(url_for('portfolio.view_portfolio'))
    
    # Pre-populate form if portfolio exists
    if artist.portfolio:  # This is now safe because we validated artist exists
        form.name.data = artist.portfolio.portfolioName
        form.description.data = artist.portfolio.description
    
    return render_template('portfolio/create.html', form=form)

@portfolio_bp.route('/manage', methods=['GET', 'POST'])
@login_required
def manage_portfolio():
    if not current_user.artist_profile:
        abort(403)
    
    form = PortfolioItemForm()
    if form.validate_on_submit():
        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], 
                    unique_filename
                )
                file.save(file_path)
                
                new_item = PortfolioItem(
                    image_url=unique_filename,
                    description=form.description.data,
                    artist_id=current_user.artist_profile.id
                )
                db.session.add(new_item)
                db.session.commit()
                flash('New portfolio item added!', 'success')
                return redirect(url_for('portfolio.manage_portfolio'))

    items = current_user.artist_profile.portfolio_items
    return render_template('portfolio/manage.html', form=form, items=items)

@portfolio_bp.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = PortfolioItem.query.get_or_404(item_id)
    if item.artist_id != current_user.artist_profile.id:
        abort(403)
    
    db.session.delete(item)
    db.session.commit()
    flash('Portfolio item deleted', 'success')
    return redirect(url_for('portfolio.manage_portfolio'))

@portfolio_bp.route('/portfolio')
@login_required
def view_portfolio():
    if not hasattr(current_user, 'artist_profile') or not current_user.artist_profile.portfolio:
        abort(404)
    return render_template('portfolio/view.html', 
                         portfolio=current_user.artist_profile.portfolio)