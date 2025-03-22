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

class Client(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    phone = db.Column(db.String(20))
    skin_type = db.Column(db.String(50))
    preferences = db.Column(db.Text)
    user = db.relationship('User', back_populates='client_profile')

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