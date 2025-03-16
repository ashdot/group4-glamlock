from person import Person
from person import db 

class Booking(db.Model): 


    #id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    bookingId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    artist_name = db.Column(db.String(20), nullable=False)
    timeslot = db.Column(db.String(20), nullable=False) 
    service = db.Column(db.String(20), nullable=False)

    def __init__(self, client_name,email,phone,artist_name,timeslot,service):

        #self.bookingId = bookingId
        self.client_name = client_name
        self.email = email
        self.phone = phone 
        self.artist_name = artist_name
        self.timeslot = timeslot 
        self.service = service 
        

    #def checkConflict(timeslot):
        

    def scheduleBooking(self):
        db.session.add(self) #used chatgpt 
        db.session.commit() 


    def cancelBooking(self):
        db.session.delete(self)  # Removes the appointment from the database
        db.session.commit()  # Commits the change


