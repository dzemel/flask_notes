"""Flask app for Notes"""
from flask import Flask, request, render_template, redirect, session, flash
from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, NoteForm

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

# if "username" not in session:
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
        return redirect(f"/users/{user.username}")
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def show_login_page():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else: 
            form.username.errors =["Invalid username/password"]

    return render_template('login.html', form=form)


@app.route("/logout")
def logout_user():
    session.pop("username", None)
    return redirect("/")

@app.route("/users/<username>")
def show_user_details_page(username):
    
    if "username" not in session:
        flash("THIS PAGE IS SECRET! YOU ARE NOT ALLOWED!!!!!")
        return redirect("/")
    else:
        user = User.query.get_or_404(username)

        # TODO - ADD notes a user has 

        return render_template("user_details.html", user=user)


@app.route("/users/<username>/delete", methods=["GET","POST"])
def delete_user(username):

    user = User.query.get_or_404(username)

    if session["username"] == user.username:

        Note.query.filter(Note.owner == user.username).delete()
        db.session.delete(user)
        db.session.commit()

        session.pop("username") 
    else:   
        flash("THIS PAGE IS SECRET! YOU ARE NOT ALLOWED!!!!!")
    return redirect("/")
    

@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note(username):

    user = User.query.get_or_404(username)

    if session["username"] == user.username:
        form = NoteForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            
            user.notes.append(Note(title=title, content=content))  

            db.session.commit()
            
            return redirect(f"/users/{user.username}")

        return render_template('add_note.html', form=form)
    else: 
        flash("THIS PAGE IS SECRET! YOU ARE NOT ALLOWED!!!!!")
        return redirect("/")
  

@app.route("/notes/<note_id>/update", methods=["GET", "POST"])
def edit_note(note_id):

    note = Note.query.get_or_404(note_id)
    user = note.user_name
    if session["username"] == user.username:
        form = NoteForm(obj=note)

        if form.validate_on_submit():
            note.title = form.title.data
            note.content = form.content.data
            db.session.commit()
            flash(f"Note {note.title} updated!")
            return redirect(f"/users/{user.username}")
        
        return render_template("edit_note.html", form=form)
    else: 
        flash("THIS PAGE IS SECRET! YOU ARE NOT ALLOWED!!!!!")
        return redirect("/")
  

@app.route("/notes/<note_id>/delete", methods=["GET", "POST"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    user = note.user_name
    if session["username"] == user.username:
        db.session.delete(note)
        db.session.commit()
        return redirect(f"/users/{user.username}")
    else:
        flash("THIS PAGE IS SECRET! YOU ARE NOT ALLOWED!!!!!")
        return redirect("/")
  
