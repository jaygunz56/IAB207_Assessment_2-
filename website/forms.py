from datetime import date
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms import DateField, TimeField, FloatField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo, Length, Regexp, NumberRange, ValidationError

ALLOWED_FILE = {'png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'}


class RegisterForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(), Length(max=50)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(max=50)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Please enter a valid email')])
    mobile = StringField('Mobile number', validators=[
        InputRequired(),
        Regexp(r'^\+?[0-9 ]{8,15}$', message='Please enter a valid mobile number')])
    street_address = StringField('Street address', validators=[InputRequired(), Length(max=200)])
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


class EventForm(FlaskForm):
    title = StringField('Event Name', validators=[InputRequired(), Length(max=100)])
    # choices get filled in from the db in the route
    category = SelectField('Category', coerce=int, validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired(), Length(max=2000)])
    image = FileField('Event Image', validators=[
        FileRequired(message='Please upload an image for the event'),
        FileAllowed(ALLOWED_FILE, message='Only png or jpg images are allowed')])

    date = DateField('Event Date', validators=[InputRequired()])
    start_time = TimeField('Start Time', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    venue_name = StringField('Venue', validators=[InputRequired(), Length(max=100)])
    venue_address = StringField('Venue Address', validators=[InputRequired(), Length(max=200)])
    parking_info = TextAreaField('Parking Information', validators=[Length(max=500)])

    ticket_type = SelectField('Ticket Type', choices=['Spectator', 'Participant Entry'])
    ticket_price = FloatField('Ticket Price', validators=[InputRequired(), NumberRange(min=0)])
    ticket_quantity = IntegerField('Tickets Available', validators=[InputRequired(), NumberRange(min=1)])

    age_restriction = SelectField('Age Restriction', choices=['All ages', '12+', '16+', '18+'])
    acknowledgement = SelectField('Acknowledgement of Country', choices=[
        ('none', 'No Acknowledgement of Country'),
        ('generic', 'Acknowledgement of Country: generic'),
        ('enhanced', 'Acknowledgement of Country: enhanced')])
    traditional_custodians = StringField('Traditional Custodians', validators=[Length(max=100)])
    acknowledgement_text = TextAreaField('Your acknowledgement', validators=[Length(max=600)])
    spectator_access = BooleanField('Spectator access is available', default=True)

    submit = SubmitField('Create Event')

    def validate_date(self, field):
        if field.data < date.today():
            raise ValidationError("Event date can't be in the past")

    def validate_end_time(self, field):
        if self.start_time.data and field.data <= self.start_time.data:
            raise ValidationError('End time needs to be after the start time')

    def validate_traditional_custodians(self, field):
        if self.acknowledgement.data == 'enhanced' and not field.data.strip():
            raise ValidationError('Add the Traditional Custodians to use the enhanced acknowledgement')


class EditEventForm(EventForm):
    # same as the create form but the image is optional when editing
    image = FileField('Event Image', validators=[FileAllowed(ALLOWED_FILE, message='Only png or jpg images are allowed')])
    submit = SubmitField('Save Changes')


class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired(), Length(max=400)])
    submit = SubmitField('Post Comment')


class BookingForm(FlaskForm):
    ticket_type = SelectField('Ticket Type', coerce=int)
    quantity = IntegerField('Number of Tickets', validators=[InputRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Book Now')
