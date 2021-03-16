"""Flask app for Notes"""
from flask import Flask, request, render_template, redirect
from models import db, connect_db, User
from forms import RegisterForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
connect_db(app)

app.config['SECRET_KEY'] = "secret"


@app.route("/")
def route_to_register_page():

    return redirect("/register")

@app.route('/register', methods = ["GET", "POST"])
def show_register_page():

    form = RegisterForm()

    if form.validate_on_submit():
        
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
      
        db.session.add(user)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('register.html', form=form)