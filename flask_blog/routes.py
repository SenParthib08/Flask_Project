from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


# list of dictionaries
posts = [
    {
        'author':'Parthib Sen',
        'title':'Blog Post 1',
        'content':'First Blog post using Flask microframework',
        'date_posted':'Dec 29, 2022'
    },
    {
        'author':'Jenna Ortega',
        'title':'Blog Post 2',
        'content':'First Blog post using Flask microframework for Wednesday',
        'date_posted':'Dec 28, 2022'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

# Creating the Register route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created and now you can login !', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)

# Creating the Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful !!', 'success')
            return  redirect(next_page) if next_page else redirect(url_for('home'))
        else:    
            flash('Login unsuccessful !! Please enter correct email and password.', 'danger')   
    return render_template('login.html', title='login', form=form)

# Creating the Logout route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))   

@app.route("/profile", methods = ['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been successfully updated !!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username    
        form.email.data = current_user.email    
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('profile.html', title = 'profile', image_file = image_file, form = form)