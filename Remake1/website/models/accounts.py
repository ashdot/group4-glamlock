from flask import flash
from .. import db 
from flask_login import  UserMixin
#from sql_alchemy.sql import func 
from werkzeug.security import generate_password_hash, check_password_hash

class UserAccount(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    firstName = db.Column(db.String(25), nullable=False)
    lastName = db.Column(db.String(25), nullable=False)
    phone = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    #password_hash = db.Column(db.String(128), nullable=False)
    accountType = db.Column(db.String(20), nullable=False) #Customer or Artist 


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

    def check_password(self, password): #TAKEN FROM CHATGPT
        return check_password_hash(self.password_hash, password)

        
    
    def createAccount(self,user):
        db.session.add(user)
        db.session.commit()
   
        



class ArtistAccount(UserAccount):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    portfolio_url = db.Column(db.String(256))

    def __init__(self,firstName,lastName,email,phone,password):

        super().__init__(firstName,lastName,email,phone,password,accountType='makeupArtist')



    def set_portfolio(self, url):
        self.portfolio_url = url


    pass




class CustomerAccount(UserAccount):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def __init__(self,firstName,lastName,email,phone,password):
        super().__init__(firstName,lastName,email,phone,password,accountType='client')
        
    pass 