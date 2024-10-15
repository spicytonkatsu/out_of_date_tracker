from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Item
from datetime import datetime, timedelta
import json

app = Flask(__name__) # initializes flask
app.config['SECRET_KEY'] = 'sfgvsbfdvjhbsryjrgjvsbjhfd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # points to an SQLite database called users.db
db.init_app(app) # connects sqlalchemy instance to flask

login_manager = LoginManager() 
login_manager.init_app(app) # connects loginManager to flask
login_manager.login_view = 'login'

@login_manager.user_loader # decorator
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html', message='This is the Calendar page.')

@app.route('/bell')
@login_required
def bell():
    return render_template('bell.html', message='This is the Notifications page.')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', message='This is the Settings page.')

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
            flash('Invalid username or password.')
            print("Invalid login attempt for username:", username)  # Debugging output
    return render_template('login.html')

@app.route('/logout') # logout endpoint
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    #items = Item.query.filter_by(user_id=current_user.id).all()
    #return render_template('dashboard.html', items=items)
    return render_template('dashboard.html')

# adding, editing, deleting operations

@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        department = request.form['department']
        upc = request.form['upc']
        image = request.form['image']
        display_duration = int(request.form['display_duration'])

        expiry_date = datetime.now() + timedelta(days=display_duration)

        new_item = Item(
            name=name, 
            brand=brand,
            department=department, 
            upc=upc, 
            image=image, 
            user_id=current_user.id,
            display_duration=display_duration,
            expiry_date=expiry_date
        )
        db.session.add(new_item)
        db.session.commit()

        flash('Item added successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_item.html')

@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.brand = request.form['brand']
        item.department = request.form['department']
        item.upc = request.form['upc']
        item.image = request.form['image']
        item.display_duration = int(request.form['display_duration'])  # Update display duration

        item.expiry_date = datetime.now() + timedelta(days=item.display_duration)

        db.session.commit()
        flash('Item updated successfully!')
        return redirect(url_for('dashboard'))

    return render_template('edit_item.html', item=item)

@app.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!')
    return redirect(url_for('dashboard'))

@app.route('/items', methods=['GET'])
@login_required
def get_items():
    with open('items.json') as f:
        items = json.load(f)
    return json.dumps(items)



if __name__ == '__main__':
    with app.app_context():
        db.create_all() # creates the database tables

        app.run(debug=True)