from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField


class RegisterForm(FlaskForm):
    firstName = StringField(label='First Name')
    lastName = StringField(label='Last Name')
    userName = StringField(label='User Name')
    password = PasswordField(label='Password')
    password_valid = PasswordField(label='Valid your password')
    email_address = EmailField(label='Email')
    submit = SubmitField(label='Submit')
