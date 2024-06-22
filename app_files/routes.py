from app_files import app, db
from flask import render_template, redirect, url_for, flash, request
from app_files.models import User
from app_files.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
import requests

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    keys = {
        "world": "World News",
        "technology": "Technology Headlines",
        "business": "Business Headlines",
        "sports": "Sports Headlines"
    }
    #api = https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey=b3ea79f80b1d46709c149fd8d0557842
    #api = https://gnews.io/api/v4/top-headlines?category=general&lang=en&country=in&apikey=1005d0c5922fe20336ea32145027ba94
    ip_country = "in"
    if current_user.is_authenticated:
        ip_country = current_user.country
    req = requests.get("https://gnews.io/api/v4/top-headlines?category=general&lang=en&country=" + ip_country + "&apikey=1005d0c5922fe20336ea32145027ba94").json()
    cases = req['articles']
    category = "None"
    header = "Headlines"

    if request.method == "POST":
        category = list(request.form)[0]

        if current_user.is_authenticated:
            if category == "technology":
                current_user.technology += 1
            elif category == "business":
                current_user.business += 1
            elif category == "sports":
                current_user.sports += 1
            db.session.commit()

        header = keys[category]

        url = "https://gnews.io/api/v4/top-headlines?category=" + category + "&lang=en&country=" + ip_country + "&apikey=1005d0c5922fe20336ea32145027ba94"
        # url = "https://newsapi.org/v2/top-headlines?country=" + ip_country + "&category=" + category + "&apiKey=b3ea79f80b1d46709c149fd8d0557842"
        req = requests.get(url).json()
        cases = req['articles']
        return render_template('news.html', cases= cases, cat= category, header = header)
    
    return render_template('news.html', cases= cases, cat= category, header = header)

@app.route('/signup', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              country=form.country.data,
                              password=form.pwd1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account created successfully! You are logged in as: {user_to_create.username}', category='success')

        return redirect(url_for('home'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'Error Exception Raised : {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.check_pwd_correction(form.password.data):
            login_user(attempted_user)
            flash(f'Login Successful! Welcome: {attempted_user.username}', category='success')

            return redirect(url_for('home'))
        else:
            flash('Username or password mismatch!', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for("home"))

@app.route('/about/<username>')
def user_page(username):
    handle = User.query.filter_by(username=username).first()

    if handle:
        return render_template('user.html', username=username, details=handle)
    else:
        flash(f'No user with username: {username} exists!', category="info")
        return render_template('user.html', username=None, details=handle)

