from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from models import User, Client, Artist, Portfolio
from forms import RegistrationForm, LoginForm
from utils import send_verification_email
from extensions import db, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            print("\n=== REGISTRATION ATTEMPT ===")
            print(f"Email: {form.email.data}")
            print(f"User Type: {form.user_type.data}")

            # Create user
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                user_type=form.user_type.data
            )
            user.set_password(form.password.data)
            print("User created:", user)

            # Create profile
            if form.user_type.data == 'client':
                profile = Client(
                    phone=form.phone.data,
                    skin_type=form.skin_type.data
                )
                user.client_profile = profile
                print("Client profile:", profile)
            else:

                portfolio = None

                profile = Artist(
                    specialization=form.specialization.data,
                    experience = None,
                    availability= None,
                    portfolio= portfolio,
                )
                user.artist_profile = profile
                print("Artist profile:", profile)

            db.session.add(user)
            print("Session add complete")
            
            db.session.commit()
            print("COMMIT SUCCESSFUL TO DATABASE")
            print(f"New User ID: {user.id}")

            flash('Account created! Please check your email', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            print("\n!!! DATABASE ERROR !!!")
            print(str(e))
            flash('Error creating account. Please try again.', 'danger')
    
    elif form.errors:
        print("\n!!! FORM ERRORS !!!")
        print(form.errors)
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/verify/<token>')
def verify_email(token):
    user = User.verify_token(token)
    if not user:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('auth.register'))
    
    user.verified = True
    db.session.commit()
    flash('Email verified! You can now login', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            print(f"Login attempt for email: {form.email.data}")
            user = User.query.filter_by(email=form.email.data).first()
            
            if not user:
                print("User not found")
                flash('Invalid credentials', 'danger')
                return redirect(url_for('auth.login'))
            
            print(f"Found user: {user.id} | Verified: {user.verified}")
            print(f"Password check: {user.check_password(form.password.data)}")
            
            if user and user.check_password(form.password.data):
                if False:  # Temporarily disable verification
                    flash('Please verify your email first', 'warning')
                    return redirect(url_for('auth.login'))
                
                login_user(user, remember=form.remember.data)
                print("Login successful!")
                return redirect(url_for('bookings.view_bookings'))
            
            flash('Invalid credentials', 'danger')
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            flash('Login failed. Please try again.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))