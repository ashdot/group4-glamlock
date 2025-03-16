
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Person(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
    firstName = db.Column(db.String(25), nullable=False)
    lastName = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, firstName, lastName, email, password):

        self.firstName =  firstName
        self.lastName = lastName 
        self.email = email 
        self.password = password 

    def updateProfile(self, firstName=None, lastName=None, email=None, password=None):

        if firstName: # used chatgpt 
            self.firstName = firstName
        if lastName:
            self.lastName = lastName
        if email:
            self.email = email
        if password:
            self.password = password
        db.session.commit()

    def createAccount(self):
        db.session.add(self) #used chatgpt 
        db.session.commit() 