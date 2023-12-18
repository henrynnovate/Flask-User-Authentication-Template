from raffle import app, bcrypt, db
from flask import flash, redirect, render_template, request, url_for
from raffle.models import User
from flask_login import login_user

# Custom Database Query Functions
def add_user(user):
   with app.app_context():
      db.session.add(user)
      db.session.commit()
def get_users():
   return User.query.all()
def username_exists(username):
   user = User.query.filter_by(username=username).first()
   return user
def email_exists(email):
   user = User.query.filter_by(email=email).first()
   return user

# Home Route --------------------------------
@app.route("/")
def homepage():
   return render_template('home.html', title='HomePage')

# Signup Route -------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
   
   # Extracting form data
   if request.method == "POST":
      username = request.form.get('username')
      email = request.form.get('email')
      password = request.form.get('password')
      hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 

      #  Check if user already exists
      username_exist_check = username_exists(username)
      email_exist_check = email_exists(email)
      if username_exist_check or email_exist_check:
         if username_exist_check:
            flash('Username exists already', 'danger')
         if email_exist_check:
            flash('Email exists already', category='danger')
         return redirect(url_for('signup'))
      
      # Adding user to database
      user = User(username=username, email=email, pwd=hashed_password)
      add_user(user)

      return redirect(url_for('homepage'))
   return render_template('signup.html', title='Signup')

# Login Route --------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

   # Extracting form data
   if request.method == 'POST':
      email_data = request.form.get('email')
      password_data = request.form.get('password')
      user = email_exists(email_data)
      if user and bcrypt.check_password_hash(user.pwd, password_data):
         login_user(user)
         return redirect(url_for('homepage'))
      else:
         flash('Login Unsuccessful. Check email and password', 'danger')
   return render_template('login.html', title='Login')