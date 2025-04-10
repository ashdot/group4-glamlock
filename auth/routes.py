from flask import Blueprint, abort, current_app, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user
from models import User, Client, Artist, Portfolio
from forms import RegistrationForm, LoginForm
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

            # Create user and add to session first
            user = User(
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),
                email=form.email.data.lower().strip(),
                user_type=form.user_type.data
            )
            user.set_password(form.password.data.strip())
            db.session.add(user)  # Add user to session before creating profile
            db.session.flush()    # Generate user ID without committing

            print("User created and added to session:", user)

            # Create profile after user is in the session
            if form.user_type.data == 'client':
                profile = Client(
                    phone=form.phone.data.strip(),
                    skin_type=form.skin_type.data.strip()
                )
                user.client_profile = profile  # Link via relationship
                print("Client profile linked:", profile)
            else:
                profile = Artist(
                    specialization=form.specialization.data.strip(),
                    experience=None,
                    availability=True
                )
                user.artist_profile = profile  # Link via relationship
                print("Artist profile linked:", profile)

            # No need to add profile explicitly; SQLAlchemy handles it via the relationship

            db.session.commit()  # Commit both user and profile together
            print("COMMIT SUCCESSFUL TO DATABASE")
            print(f"New User ID: {user.id}")

            user.verified = True  # Auto-verify users
            flash('Account created successfully!', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            db.session.rollback()
            print("\n!!! DATABASE ERROR !!!")
            print(str(e))
            flash('Error creating account. Please try again.', 'danger')
    
    elif form.errors:
        print("\n!!! FORM ERRORS !!!")
        print(form.errors)
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            print(f"Login attempt for email: {form.email.data}")
            user = User.query.filter(db.func.lower(User.email) == form.email.data.lower().strip()).first()
            
            if not user:
                print("User not found")
                flash('Invalid credentials', 'danger')
                return redirect(url_for('auth.login'))
            
            print(f"Found user: {user.id}")
            
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                print("Login successful!")
                return redirect(url_for('home'))
            
            print("Invalid password")
            flash('Invalid credentials', 'danger')
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            flash('Login failed. Please try again.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/dev/login', methods=['POST'])
def dev_login():
    if not current_app.config['DEV_MODE']:
        abort(403)
        
    dev_key = request.form.get('dev_key')
    if dev_key != current_app.config['DEV_KEY']:
        flash('Invalid developer key', 'danger')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/dev_access.html')

@auth_bp.route('/dev/login/as/<role>')
def dev_login_as(role):
    if not current_app.config['DEV_MODE']:
        abort(403)
    
    demo_email = f"demo_{role}@glamlock.dev"
    user = User.query.filter_by(email=demo_email).first()
    
    if not user:
        user = User(
            first_name="Demo",
            last_name=role.title(),
            email=demo_email,
            user_type=role,
        )
        user.set_password('demo_password')
        
        if role == 'artist':
            profile = Artist(
                specialization="Demo Artist",
                experience=5,
                availability=True
            )
            user.artist_profile = profile
        else:
            profile = Client(
                phone="123-456-7890",
                skin_type="Combination",
                preferences="Demo preferences"
            )
            user.client_profile = profile
            
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    flash(f'Logged in as demo {role}', 'success')
    return redirect(url_for('home'))