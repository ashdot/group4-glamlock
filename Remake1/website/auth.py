from flask import Blueprint , render_template, redirect, url_for, request, flash
from . import db 
from .models import UserAccount, CustomerAccount, ArtistAccount
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth",__name__)

@auth.route("/login")
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = UserAccount.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user, remember=True)
                flash('You are now logged in!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrect.', category='error')

        else:
            flash('Email does not exist', category='error')

        return render_template("login.html")

@auth.route("/sign-up", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        accountType = request.form.get("accountType")


        User = UserAccount(firstName=firstName, lastName=lastName,email=email,phone=phone,password=generate_password_hash(password, method='sha256'),accountType=accountType)

        User.validateEmail(email)
        User.validatePassword(password,password2)

        if accountType == 'client':
            user = CustomerAccount(User)
        elif accountType == 'makeupArtist':
            user = ArtistAccount(User)
        else:
            return flash('Error, No account Type', category='error')
        
        

        print(firstName)
        print(lastName)
        print(email)
        print(phone)
        print(password)
        print(password2)
        print(accountType)
        

        User.createAccount(user)
        flash('Account Created', category='success')

        return redirect(url_for('views.home'))









    return render_template("signup.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
