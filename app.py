from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required
from extensions import db, bcrypt, login_manager, mail, migrate
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-123'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'glamlock.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=False,  # Disabled database query logging
    )
    
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', '')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER', 'noreply@glamlockja.com') 
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
    app.config['DEV_MODE'] = True  # Set to False when not testing
    app.config['DEV_KEY'] = 'glamlock_dev_2025'  

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Login manager configuration
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return db.session.get(User, int(user_id))

    # Register blueprints
    from artists.routes import artists_bp
    from auth.routes import auth_bp
    from bookings.routes import bookings_bp
    from events.routes import events_bp
    from portfolio.routes import portfolio_bp
    from products.routes import products_bp
    from recommendations.routes import recommendations_bp
    app.register_blueprint(artists_bp, url_prefix='/artists')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(bookings_bp, url_prefix='/bookings')
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(recommendations_bp, url_prefix='/recommendations')

    # Database setup
    with app.app_context():
        from models import User, Artist, Client, Booking, Portfolio
        db.create_all()

    # Core routes
    @app.route('/')
    def index():
        return redirect(url_for('home'))

    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html')

    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', user=current_user)

    # Debug routes
    '''
    @app.route('/test-template')
    def test_template():
        return render_template('auth/login.html')
    
    @app.route('/users')
    def list_users():
        from models import User
        users = User.query.all()
        return render_template('users.html', users=users)
    
    @app.route('/db-test')
    def db_test():
        from models import User
        users = User.query.all()
        return f"Total users: {len(users)}"
    
    @app.route('/db-check')
    def db_check():
        try:
            db.session.execute('SELECT 1')
            return 'Database connection working', 200
        except Exception as e:
            return f'Database error: {str(e)}', 500
    '''

    return app

if __name__ == '__main__':
    app = create_app()
    # Run with debug mode based on environment variable
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')