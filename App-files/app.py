from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate

from person import db 
from makeupartist import MakeupArtist
from customer import Customer  
from customer import Person
from makeupartist import Person
from booking import Booking
from consultation import Consultation 




app = Flask(__name__)

app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)


with app.app_context():
    db.create_all()
    db.session.commit()
    print('Database created')

@app.route('/')
def test():
    return render_template('test.html')

"""
@app.route('/signup', methods =['GET', 'POST'])
def addAccount():
    #msg = ''
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        phone = request.form['phoneNumber']
        password = request.form['password']
        password2 = request.form['password2']

        nameType = request.form['nameType']


        if password != password2 :
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('test')) 
            
        new_user = Person(firstName=firstName,lastName=lastName,email=email,password=password)

        #if nameType == "MakeupArtist":
            #new_user = MakeupArtist(person)
        
        #if nameType == "Customer":
            #new_user = Customer(person)

    
    new_user.createAccount()
    flash('Account created successfully!', 'success')
    return redirect(url_for('test')) """


@app.route('/signup', methods=['GET', 'POST'])
def addAccount():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        phone = request.form['phoneNumber']
        password = request.form['password']
        password2 = request.form['password2']
        nameType = request.form['nameType']

        if password != password2:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('test'))
            
        new_user = Person(firstName=firstName, lastName=lastName, email=email, password=password)

        try:
            # These operations must be inside the POST block
            new_user.createNewAccount()
            flash('Account created successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'error')
            
        return redirect(url_for('addAccount'))
    
    # Return template for GET requests
    return render_template('test.html')  # Adjust template name as needed

@app.route('/appoint', methods=['GET', 'POST'])
def addAppointment():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        artist = request.form['artist']
        timeslot = request.form['timeslot']
        service = request.form['service']
     
        # Create new booking
        new_booking = Booking(client_name=name, email=email, phone=phone, artist_name=artist, timeslot=timeslot, service=service)
        
        
        new_booking.scheduleBooking()
        flash("Appointment booked successfully!", "success")          
        return redirect(url_for('addAppointment'))
    
    # Return template for GET requests
    return render_template('appoint.html')


"""
     
@app.route('/appoint', methods=['GET', 'POST'])
def bookAppointment():
    if request.method == 'POST':
        try:
            # Get form data with validation
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            artist = request.form.get('artist')
            timeslot = request.form.get('timeslot')
            service = request.form.get('service')
            
            # Basic validation
            if not all([name, email, phone, artist, timeslot, service]):
                flash("All fields are required", "error")
                # Replace 'appointment_page' with your actual route function name
                return redirect(url_for('appoint'))
                
            # Check if an appointment already exists for this artist and timeslot
            existing_booking = Booking.query.filter_by(artist_name=artist, timeslot=timeslot).first()
            
            if existing_booking:
                flash("This timeslot is already booked for the selected artist. Please choose another time.", "error")
                return redirect(url_for('appoint'))
            
            # Create new booking
            new_booking = Booking(
                client_name=name,
                email=email,
                phone=phone,
                artist_name=artist,
                timeslot=timeslot,
                service=service
            )
            
            # Use a try-except block around database operations
            try:
                db.session.add(new_booking)
                db.session.commit()
                # Only call scheduleBooking after successfully adding to database
                new_booking.scheduleBooking()
                flash("Appointment booked successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error booking appointment: {str(e)}", "error")
                
            return redirect(url_for('appoint'))
            
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", "error")
            return redirect(url_for('appoint'))
            
    # If GET request, redirect to appointment page
    return redirect(url_for('appoint')) """
     


     #wanted to add smt where if they book depending on the service it would create either a Consultation or a Appointment 



      
@app.route('/show-users')
def show_users():
    users = Person.query.all()
    return render_template('users.html', users=users)

@app.route('/show-bookings')
def show_bookings():
    bookings = Booking.query.all()
    return render_template('bookings.html', bookings=bookings)






    
if __name__ == '__main__':
    app.run(debug=True)