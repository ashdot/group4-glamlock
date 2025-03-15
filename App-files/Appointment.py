from person import Person
from person import db 

class Appointment: 

    __tablename__ = 'appointment'
    
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    bookingId = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True)  # Auto-generated ID
    bookingDate = db.Column(db.String(20), nullable=False)
    skin_type = db.Column(db.String(20), nullable=False)
    def __init__(self, bookingId, bookingDate, status, preferences):


        self.bookingId = bookingId
        self.bookingDate = bookingDate
        self.notes = status
        self.preferences = preferences 

    def scheduleAppointment(self):


        pass


    def cancelAppointment(self):
        pass