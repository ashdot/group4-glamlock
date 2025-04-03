from person import Person

from person import db 


class MakeupArtist(Person): #Inherits from Person class 
    __tablename__ = 'makeup_artist'

    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    artistId = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True)  # Auto-generated ID 
    experience_years = db.Column(db.Integer, nullable=True)
    specialization = db.Column(db.String(100), nullable=True)
    availablity = db.Column(db.String(200), nullable=True)

    def __init__(self, firstName, lastName, email, password, phone, artistId, specialization, availability):
        
        super().__init__(firstName, lastName, email, password, phone)

        self.artistId =  artistId
        self.specialization = specialization 
        self.availablity = availability
        