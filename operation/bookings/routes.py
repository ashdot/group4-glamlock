from flask import Blueprint, abort, current_app, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import User, db, Booking, Artist
from forms.forms import BookingForm, EditBookingForm

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = BookingForm()
    
    artists = Artist.query.join(User).filter(Artist.availability == True).all()
    form.artist_id.choices = [(a.id, f"{a.user.first_name} {a.user.last_name}") for a in artists]

    if form.validate_on_submit():
        try:
            booking = Booking(
                user_id=current_user.id,
                artist_id=int(form.artist_id.data),
                service_type=form.service_type.data,
                datetime=form.datetime.data,
                notes=form.notes.data,
                status='pending'
            )
            
            db.session.add(booking)
            db.session.commit()
            flash('Booking created successfully!', 'success')
            return redirect(url_for('bookings.view_bookings'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating booking: {str(e)}', 'danger')
            current_app.logger.error(f'Booking error: {str(e)}')

    if form.errors:
        current_app.logger.error(f'Form errors: {form.errors}')
        flash('Please correct the form errors', 'danger')
    
    return render_template('bookings/book.html', form=form, artists=artists)

@bookings_bp.route('/bookings')
@login_required
def view_bookings():
    bookings = current_user.client_bookings
    return render_template('bookings/bookings.html', bookings=bookings)

@bookings_bp.route('/artist-bookings')
@login_required
def artist_bookings():
    if not hasattr(current_user, 'artist_profile'):
        abort(403)
    
    bookings = Booking.query.filter_by(
        artist_id=current_user.artist_profile.id
    ).order_by(Booking.datetime.desc()).all()
    
    return render_template('bookings/artist_bookings.html', bookings=bookings)

@bookings_bp.route('/edit-booking/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if not current_user.artist_profile or booking.artist_id != current_user.artist_profile.id:
        abort(403)
    
    form = EditBookingForm(obj=booking)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(booking)
            db.session.commit()
            flash('Booking updated successfully!', 'success')
            return redirect(url_for('bookings.artist_bookings'))
        except Exception as e:
            db.session.rollback()
            flash(f'Update error: {str(e)}', 'danger')
    
    return render_template('bookings/edit_booking.html', form=form, booking=booking)

@bookings_bp.route('/delete-booking/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if not current_user.artist_profile or booking.artist_id != current_user.artist_profile.id:
        abort(403)
    
    try:
        db.session.delete(booking)
        db.session.commit()
        flash('Booking deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Deletion error: {str(e)}', 'danger')
    
    return redirect(url_for('bookings.artist_bookings'))