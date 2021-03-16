from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField
from wtforms.validators import Email, InputRequired, DataRequired, Length
import email_validator

class RegisterForm(FlaskForm):
    """ Form for Register User """

    username = StringField("Choose a Username", validators=[InputRequired(), DataRequired(), Length(max=20)])
    password = PasswordField("Create a Password", validators=[InputRequired(), DataRequired()])
    email = StringField("Enter Your Email", validators= [InputRequired(), DataRequired(), Length(max=50), Email()])
    first_name = StringField("Please Enter Your First Name", validators=[InputRequired(), DataRequired(), Length(max=30)])
    last_name = StringField("Please Enter Your Last Name", validators=[InputRequired(), DataRequired(), Length(max=30)])