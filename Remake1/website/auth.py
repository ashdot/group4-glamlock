from flask import Blueprint , render_template, redirect, url_for, request, flash
from . import db 
from .models import UserAccount
auth = Blueprint("auth",__name__)

@auth.route("/login")
def login():
    email = request.form.get("email")
    password = request.form.get("password")
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

        
        User = UserAccount()

        User.validateEmail 
        User.validatePassword 

        User = UserAccount(firstName=firstName, lastName=lastName,email=email,phone=phone,password=password,accountType=accountType)
        



        print(firstName)
        print(lastName)
        print(email)
        print(phone)
        print(password)
        print(password2)
        print(accountType)





    return render_template("signup.html")

@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))
