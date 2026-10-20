from datetime import datetime, date
from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(200), nullable=False)

    events = db.relationship('Event', backref='creator')
    bookings = db.relationship('Booking', backref='user')
    comments = db.relationship('Comment', backref='user')

    def __repr__(self):
        return f"Name: {self.first_name} {self.last_name}"


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    events = db.relationship('Event', backref='category')

    def __repr__(self):
        return f"Category: {self.name}"


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    events = db.relationship('Event', backref='venue')

    def __repr__(self):
        return f"Venue: {self.name}"


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(400), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    # Open, Sold Out, Cancelled or Inactive
    status = db.Column(db.String(20), default='Open')
    age_restriction = db.Column(db.String(10), default='All ages')
    spectator_access = db.Column(db.Boolean, default=True)
    parking_info = db.Column(db.Text)
    # none, generic or enhanced
    acknowledgement = db.Column(db.String(20), default='none')
    # only used for the enhanced acknowledgement
    traditional_custodians = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))

    ticket_types = db.relationship('TicketType', backref='event', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='event', cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='event')

    def update_status(self):
        # cancelled is set by the organiser so leave it alone
        if self.status == 'Cancelled':
            return

        now = datetime.now()
        if self.date < date.today() or (self.date == date.today() and self.end_time < now.time()):
            self.status = 'Inactive'
            return

        tickets_left = 0
        for ticket in self.ticket_types:
            tickets_left = tickets_left + ticket.quantity_available

        if tickets_left == 0:
            self.status = 'Sold Out'
        else:
            self.status = 'Open'

    def __repr__(self):
        return f"Event: {self.title}"


class TicketType(db.Model):
    __tablename__ = 'ticket_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    bookings = db.relationship('Booking', backref='ticket_type')

    def __repr__(self):
        return f"Ticket: {self.name} ${self.price}"


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    ticket_type_id = db.Column(db.Integer, db.ForeignKey('ticket_types.id'))

    @property
    def reference(self):
        return 'TM-' + str(10000 + self.id)

    def __repr__(self):
        return f"Booking: {self.reference}"


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"
