from flask import flash
from .. import db 
from flask_login import  UserMixin
#from sql_alchemy.sql import func 

class UserAccount(db.Model,UserMixin):

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    firstName = db.Column(db.String(25), nullable=False)
    lastName = db.Column(db.String(25), nullable=False)
    phone = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    accountType = db.Column(db.String(20), nullable=False)


    def __init__(self,firstName,lastName,email,phone,password,accountType):
        self.firstName = firstName
        self.lastName = lastName 
        self.email = email 
        self.phone = phone
        self.password = password
        self.accountType = accountType

    
    def validateEmail(self,email):
        invalid_email = UserAccount.query.filter_by(email).first()
        if len(email) < 10:
            flash('Email is too short.', catergory = 'error')
        elif invalid_email:
            flash('Email is already in use.', catergory = 'error')
        
    def validatePassword(self,password1,password2):
        if password1 != password2:
            flash('Passwords do not match', catergory ='error')
        elif len(password1) < 8 :
            flash('Password is too short', catergory ='error')

    
    def createArtistAccount(self, firstName, lastName, email, phone, password ,accountType):
        if accountType == "makeupArtist":
            Artist = ArtistAccount() #Create an Artist Object and store it in Artist database Table
        pass 


    def createCustomerAccount(self, firstName, lastName, email, phone, password, accountType):
        if accountType == "client":
            Customer = CustomerAccount() #Creates a Customer Object and stores it in Customer database Table 
        pass
        



class ArtistAccount(UserAccount):




    def __init__(self,firstName,lastName,email,phone,password,accountType):

        super().__init__(firstName,lastName,email,phone,password,accountType)


    pass




class CustomerAccount(UserAccount):


    def __init__(self,firstName,lastName,email,phone,password,accountType):
        super().__init__(firstName,lastName,email,phone,password,accountType)
        
    pass 