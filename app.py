from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User

app = Flask(__name__) # initializes flask
app.config['SECRET_KEY'] = 'fuyergweyugbwer67f4trgfuyrgfey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # points to an SQLite database called users.db
db.init_app(app) # connects sqlalchemy instance to flask

login_manager = LoginManager() 
login_manager.init_app(app) # connects loginManager to flask

@login_manager.user_loader # decorator
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists!')
            return redirect(url_for('register'))

        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST']) # login endpoint
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password): # finds the user and checks if password matches
            login_user(user) # logs in
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.') # error if invalid
    return render_template('login.html')

@app.route('/logout') # logout endpoint
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # creates the database tables

        app.run(debug=True)