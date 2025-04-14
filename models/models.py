from flask import current_app
from extensions import db, bcrypt
print("Imported successfully!")

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
    portfolio = db.relationship('Portfolio', back_populates='artist', uselist=False, cascade='all, delete-orphan')
    portfolio_items = db.relationship('PortfolioItem', backref='artist', cascade='all, delete-orphan')
    events = db.relationship('Event', backref='artist', lazy=True)

    def show_artist_info(self):
        print(f"Specialization: {self.specialization}")
        print(f"Experience: {self.experience} years")
        if self.portfolio:
            print("Portfolio Details:")
            self.portfolio.showPortfolio()
        else:
            print("No portfolio available.")

    

class Client(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    phone = db.Column(db.String(20), nullable=False) 
    skin_type = db.Column(db.String(50), nullable=False)  
    preferences = db.Column(db.Text)
    user = db.relationship('User', back_populates='client_profile')
    events = db.relationship('Event', backref='client', lazy=True)

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

    def __init__(self, portfolioName, description, url):
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

class PortfolioItem(db.Model):
    __tablename__ = 'portfolio_item'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    __tablename__ = 'event'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)  
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(120))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    event_type = db.Column(db.String(30))
    
    def __init__(self, title, start_time, end_time, artist_id, 
                 event_type, description=None, location=None, client_id=None):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.artist_id = artist_id
        self.client_id = client_id
        self.event_type = event_type
    
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
    
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    artist = db.relationship('Artist', backref='products')

class ProductRecommendation(db.Model):
    __tablename__ = 'product_recommendation'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    recommended_at = db.Column(db.DateTime, default=datetime.utcnow)