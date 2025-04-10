import os
import uuid
from flask import Blueprint, abort, current_app, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from models import Product
from forms import ProductForm
from extensions import db
from werkzeug.utils import secure_filename
from utils import allowed_file

products_bp = Blueprint('products', __name__)

@products_bp.route('/artist/products')
@login_required
def manage_products():
    if not current_user.artist_profile:
        abort(403)
    products = current_user.artist_profile.products
    return render_template('products/manage.html', products=products)

@products_bp.route('/artist/products/new', methods=['GET', 'POST'])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        # Handle file upload
        if 'image' not in request.files:
            flash('No file selected', 'danger')
            return redirect(request.url)
            
        file = request.files['image']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], 
                unique_filename
            ))
            
            # Create product with filename
            product = Product(
                artist_id=current_user.artist_profile.id,
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                image_filename=unique_filename  # Store filename instead of URL
            )
            
            db.session.add(product)
            db.session.commit()
            flash('Product created!', 'success')
            return redirect(url_for('products.manage_products'))
    
    return render_template('products/create.html', form=form)

@products_bp.route('/artist/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.artist_id != current_user.artist_profile.id:
        abort(403)
    
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        # Handle image update
        if form.image.data:
            file = form.image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file.save(os.path.join(
                    current_app.config['UPLOAD_FOLDER'], 
                    unique_filename
                ))
                product.image_filename = unique_filename

        # Update other fields
        form.populate_obj(product)
        db.session.commit()
        flash('Product updated!', 'success')
        return redirect(url_for('products.manage_products'))
    
    return render_template('products/edit.html', form=form, product=product)