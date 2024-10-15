from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy() # initializes an instance of the SQLAlchemy class

class User(db.Model): # defines a User class that inherits from db.Model, each instance is a row in the users table
    id = db.Column(db.Integer, primary_key=True) # defines a column named "id"
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False) # string with max 150 characters, must be unique, and cannot be null
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)  # New field
    last_name = db.Column(db.String(100), nullable=False)   # New field

    @property
    def is_active(self):
        return True  # Assuming all users are active; modify as needed

    @property
    def is_authenticated(self):
        return True  # This should return True if the user is authenticated

    @property
    def is_anonymous(self):
        return False  # This should return False for regular users
    
    def get_id(self):
        return str(self.id)  # Flask-Login expects this to return a string

    def set_password(self, password): # defines a method that takes password as an argument
        self.password_hash = generate_password_hash(password) # hashes the plaintext password and stores it in password.hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # compares the stored hash with the provided password and returns a boolean
