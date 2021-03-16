"""Flask app for Notes"""
from flask import Flask, request, render_template, redirect, session, flash
from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
connect_db(app)

app.config['SECRET_KEY'] = "secret"


@app.route("/")
def route_to_register_page():

    return redirect("/register")

@app.route('/register', methods=["GET", "POST"])
def show_register_page():

    form = RegisterForm()

    if form.validate_on_submit():
        
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username
        return redirect('/secret')
    else:
        return render_template('register.html', form=form)


@app.route("/secret")
def show_secret_page():
    
    if "username" not in session:
        flash("THIS PAGE IS SECRET! YOU ARE NOT ALLOWED!!!!!")
        return redirect("/")
    else:
        return render_template("secret.html")


@app.route('/login', methods=["GET", "POST"])
def show_login_page():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect("/secret")
        else: 
            form.username.errors =["Invalid username/password"]

    return render_template('login.html', form=form)


@app.route("/logout")
def logout_user():
    session.pop("username", None)
    return redirect("/")

# @app.route("/users/<int:user_id")