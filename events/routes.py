from flask import Blueprint, abort, current_app, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from models import Event, db 


events_bp = Blueprint('events', __name__)

# Manage Events (Create & View)
@events_bp.route('/event', methods=['GET', 'POST'])
@login_required
def manage_events():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        location = request.form.get('location')
        artist_name = request.form.get('artist_name')
        event_type = request.form.get('event_type')
        client_email = request.form.get('client_email')

        if not all([title, start_time, end_time, artist_name, event_type]):
            flash("Missing required fields.", "error")
            return redirect(url_for('manage_events'))

        new_event = Event(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            artist_name=artist_name,
            event_type=event_type,
            client_email=client_email
        )

        try:
            db.session.add(new_event)
            db.session.commit()
            flash("Event created successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating event: {str(e)}", "error")

        return redirect(url_for('manage_events'))

    events = Event.query.all()
    return render_template('events/event.html', events=events) 

# Update an Event
@events_bp.route('/events/update/<int:event_id>', methods=['POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)

    title = request.form.get('title')
    description = request.form.get('description')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    location = request.form.get('location')
    artist_name = request.form.get('artist_name')
    event_type = request.form.get('event_type')
    client_email = request.form.get('client_email')

    try:
        event.updateEvent(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            artist_name=artist_name,
            event_type=event_type,
            client_email=client_email
        )
        flash("Event updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating event: {str(e)}", "error")

    return redirect(url_for('manage_events'))

# Delete an Event
@events_bp.route('/events/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    try:
        db.session.delete(event)
        db.session.commit()
        flash("Event deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting event: {str(e)}", "error")

    return redirect(url_for('manage_events'))