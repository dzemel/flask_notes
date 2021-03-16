from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField
from wtforms.validators import Email, InputRequired, DataRequired, Length
import email_validator

class RegisterForm(FlaskForm):
    """ Form for Register User """

    username = StringField("Choose a Username",
                           validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Create a Password", 
                             validators=[InputRequired()])
    email = StringField("Enter Your Email",
                        validators=[InputRequired(), Length(max=50), Email()])
    first_name = StringField("Please Enter Your First Name",
                             validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Please Enter Your Last Name",
                            validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Formm for Loggin in User"""
    username = StringField("Username", 
                           validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", 
                             validators=[InputRequired()])

class NoteForm(FlaskForm):
    """Form for Taking Notes"""
    title = StringField("title", validators=[InputRequired(), Length(max=100)])

    content = TextField("content", validators=[InputRequired()])
    