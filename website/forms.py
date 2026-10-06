from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length, Regexp


class RegisterForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(), Length(max=50)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(max=50)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Please enter a valid email')])
    mobile = StringField('Mobile number', validators=[
        InputRequired(),
        Regexp(r'^\+?[0-9 ]{8,15}$', message='Please enter a valid mobile number')])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8, message='Password needs to be at least 8 characters')])
    confirm = PasswordField('Confirm password', validators=[
        InputRequired(),
        EqualTo('password', message='Passwords should match')])
    submit = SubmitField('Create account')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log in')
