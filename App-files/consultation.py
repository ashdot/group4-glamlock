from person import Person

from person import db 

class Consultation: 

    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    consultationId = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True) 
    date = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(20), nullable=True)
    preferences = db.Column(db.String(100), nullable=True)
    confirmed = db.Column(db.Boolean, default=False)


    def __init__(self, consultationId, date, notes, preferences):

        self.consultationId = consultationId
        self.date = date
        self.notes = notes
        self.preferences = preferences 

    def addConsultation(self):
        db.session.add(self) 
        db.session.commit() 

    def updatePreferences(self,preferences):
        self.preferences = preferences
        db.session.commit()

    def viewPreferences(self):
        return self.preferences

    def confirmConsultation(self):
        self.confirmed = True
        db.session.commit()
    
