from person import Person
from person import db 


class Customer(Person): #Inherits from Person class
    
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    customerId = db.Column(db.Integer, unique=True, nullable=False, autoincrement=True)  # Auto-generated ID
    #phone_number = db.Column(db.String(20), nullable=False)
    skin_type = db.Column(db.String(20), nullable=True)



    def __init__(self, firstName, lastName, email, password, phone, customerId,skinType):
        
        super().__init__(firstName, lastName, email, password, phone)

        self.customerId =  customerId
        self.skinType = skinType
        #self.phoneNumber = phoneNumber

        