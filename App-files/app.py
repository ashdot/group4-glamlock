from flask import Flask, render_template, request, redirect, url_for, flash

from person import db 
from makeupartist import MakeupArtist
from customer import Customer  
from customer import Person
from makeupartist import Person





app = Flask(__name__)

app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


with app.app_context():
    db.create_all()
    db.session.commit()
    print('Database created')

@app.route('/')
def test():
    return render_template('test.html')


@app.route('/signup', methods =['GET', 'POST'])
def addAccount():
    #msg = ''
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        phone = request.form['phoneNumber']
        password = request.form['password']
        password2 = request.form['password2']
        #artist = request.form.get['artist']
        #customer = request.form.get['client']

        if password != password2 :
            flash('Passwords do not match. Please try again.', 'error')
            #msg = 'Passwords do not match'
            return redirect(url_for('test')) 
            
        new_user = Person(firstName=firstName,lastName=lastName,email=email,password=password)

        #if artist:
            #new_user = MakeupArtist(person)
        
        #if customer:
            #new_user = Customer(person)

    
    new_user.createAccount()
    flash('Account created successfully!', 'success')
    return redirect(url_for('test'))

      
@app.route('/show-users')
def show_users():
    users = Person.query.all()
    return render_template('users.html', users=users)


    
if __name__ == '__main__':
    app.run(debug=True)