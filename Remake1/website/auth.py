from flask import Blueprint , render_template, redirect, url_for, request

auth = Blueprint("auth",__name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/sign-up", methods=['GET','POST'])
def signup():
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    accountType = request.form.get("accountType")

    print(firstName)
    print(lastName)
    print(email)
    print(password)
    print(password2)
    print(accountType)



    return render_template("signup.html")

@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))
