from datetime import datetime
from flask import Blueprint, abort, current_app, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from models.models import Event, db

events_bp = Blueprint('events', __name__)

@events_bp.route('/manage', methods=['GET', 'POST'])
@login_required
def manage_events():
    if not current_user.artist_profile:
        abort(403)
        
    if request.method == 'POST':
        try:
            # Required fields
            title = request.form.get('title')
            start_time = datetime.fromisoformat(request.form.get('start_time'))
            end_time = datetime.fromisoformat(request.form.get('end_time'))
            event_type = request.form.get('event_type')
            
            if not all([title, start_time, end_time, event_type]):
                flash("Missing required fields", "error")
                return redirect(url_for('events.manage_events'))

            # Create event with current artist
            new_event = Event(
                title=title,
                start_time=start_time,
                end_time=end_time,
                event_type=event_type,
                artist_id=current_user.artist_profile.id,
                description=request.form.get('description'),
                location=request.form.get('location')
            )

            db.session.add(new_event)
            db.session.commit()
            flash("Event created successfully!", "success")
            return redirect(url_for('events.manage_events'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error creating event: {str(e)}", "error")
            return redirect(url_for('events.manage_events'))

    # Get events for current artist
    events = Event.query.filter_by(artist_id=current_user.artist_profile.id).all()
    return render_template('events/event.html', events=events)

@events_bp.route('/update/<int:event_id>', methods=['POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Verify ownership
    if event.artist_id != current_user.artist_profile.id:
        abort(403)

    try:
        # Update fields
        event.title = request.form.get('title')
        event.description = request.form.get('description')
        event.start_time = datetime.fromisoformat(request.form.get('start_time'))
        event.end_time = datetime.fromisoformat(request.form.get('end_time'))
        event.location = request.form.get('location')
        event.event_type = request.form.get('event_type')
        
        db.session.commit()
        flash("Event updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating event: {str(e)}", "error")

    return redirect(url_for('events.manage_events'))

@events_bp.route('/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if event.artist_id != current_user.artist_profile.id:
        abort(403)

    try:
        db.session.delete(event)
        db.session.commit()
        flash("Event deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting event: {str(e)}", "error")

    return redirect(url_for('events.manage_events'))