from flask import current_app
from extensions import db, bcrypt
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.String(20))  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    client_profile = db.relationship('Client', back_populates='user', uselist=False, cascade='all, delete-orphan')
    artist_profile = db.relationship('Artist', back_populates='user', uselist=False, cascade='all, delete-orphan')
    client_bookings = db.relationship('Booking', back_populates='client', lazy=True)
    
    

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def get_reset_token(self, expires_sec=1800):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_sec)
        return serializer.dumps({'user_id': self.id})

    @staticmethod
    def verify_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
            user_id = data['user_id']
        except:
            return None
        return db.session.get(User, user_id)

class Artist(db.Model):
    __tablename__ = 'artist'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    specialization = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    availability = db.Column(db.Boolean, default=True)
   
    
    # Relationships
    user = db.relationship('User', back_populates='artist_profile')
    artist_bookings = db.relationship('Booking', back_populates='artist', lazy=True)
    artist_consultation = db.relationship('Consultation', back_populates = 'artist', lazy = True)
    


    #One Artist has One Porftolio 
    portfolio = db.relationship('Portfolio', back_populates='artist', uselist=False, cascade='all, delete-orphan')



    def __init__(self, specialization, experience, availability, portfolio):
        self.specialization = specialization
        self.experience = experience
        self.availability = availability 
        self.portfolio = portfolio #references the portfolio class 

    def show_artist_info(self):
        print(f"Specialization: {self.specialization}")
        print(f"Experience: {self.experience} years")
        if self.portfolio:
            print("Portfolio Details:")
            self.portfolio.showPortfolio()
        else:
            print("No portfolio available.")

    

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    phone = db.Column(db.String(20))
    skin_type = db.Column(db.String(50))
    preferences = db.Column(db.Text)
    user = db.relationship('User', back_populates='client_profile')
    client_consultation = db.relationship('Consultation', back_populates = 'client', lazy = True)

class Booking(db.Model):
    __tablename__ = 'booking'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    service_type = db.Column(db.String(50))
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)

    # Relationships
    client = db.relationship('User', foreign_keys=[user_id], back_populates='client_bookings')
    artist = db.relationship('Artist', foreign_keys=[artist_id], back_populates='artist_bookings')


class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    
    id = db.Column(db.Integer, primary_key=True)
    portfolioName = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(200), nullable=True)

    #Connection to Artist Table 
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    
    #Relationship to Artist 
    artist = db.relationship('Artist', back_populates='portfolio')

    def __init__(self, portfolioName, description,url):
        self.portfolioName = portfolioName
        self.description = description 
        self.url = url 

    
    def updatePortfolio(self, portfolioName, url, description):
        self.portfolioName = portfolioName
        self.url = url
        self.description = description 

    def removePortfolio(self):
        db.session.delete(self)
        db.session.commit()

    def showPortfolio(self):
        print(f"Portfolio Name: {self.portfolioName}")
        print(f"Description: {self.description}")
        print(f"Portfolio URL: {self.url}")


class Event(db.Model):
    __tablename__ = 'event'
    
    eventId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.String(30), nullable=False)  
    end_time = db.Column(db.String(30), nullable=False)    
    location = db.Column(db.String(120), nullable=True)
    artist_name = db.Column(db.String(50), nullable=False) 
    client_email = db.Column(db.String(50), nullable=True) 
    event_type = db.Column(db.String(30), nullable=False)  
    
    def __init__(self, title, description, start_time, end_time, location, artist_name, event_type, client_email=None):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.artist_name = artist_name
        self.event_type = event_type
        self.client_email = client_email
    
    def createEvent(self):
        db.session.add(self)
        db.session.commit()
    
    def updateEvent(self, title=None, description=None, start_time=None, end_time=None, 
                    location=None, artist_name=None, event_type=None, client_email=None):
        if title:
            self.title = title
        if description:
            self.description = description
        if start_time:
            self.start_time = start_time
        if end_time:
            self.end_time = end_time
        if location:
            self.location = location
        if artist_name:
            self.artist_name = artist_name
        if event_type:
            self.event_type = event_type
        if client_email is not None:  
            self.client_email = client_email
        
        db.session.commit()
    
    def cancelEvent(self):
        db.session.delete(self)
        db.session.commit()
    
    def checkTimeConflict(self, artist_name, start_time, end_time):
        """Check if there's a time conflict for the artist"""
        conflicts = Event.query.filter(
            Event.artist_name == artist_name,
            Event.eventId != self.eventId,  
            ((Event.start_time <= start_time) & (Event.end_time > start_time)) |  
            ((Event.start_time < end_time) & (Event.end_time >= end_time)) |      
            ((Event.start_time >= start_time) & (Event.end_time <= end_time))     
        ).all()
        
        return len(conflicts) > 0
    
    @staticmethod
    def getEventsByArtist(artist_name):
        return Event.query.filter_by(artist_name=artist_name).all()
    
    @staticmethod
    def getEventsByClient(client_email):
        return Event.query.filter_by(client_email=client_email).all()

class Consultation(db.Model):
    __tablename__ = 'consultations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    preferences = db.Column(db.Text, nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)

    client = db.relationship('User', foreign_keys=[user_id], back_populates ='client_consultation')
    artist = db.relationship('Artist',foreign_keys=[artist_id],  back_populates ='artist_consultation')
