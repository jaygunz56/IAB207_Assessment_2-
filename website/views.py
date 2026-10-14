from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from .models import Event, Category, Booking
from . import db

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    categories = Category.query.order_by(Category.name).all()
    selected = request.args.get('category')

    # only show events that haven't happened yet, soonest first
    events = Event.query.filter(Event.date >= date.today())

    if selected:
        # filtering by category only shows events you can still book
        events = events.join(Category).filter(Category.name == selected, Event.status == 'Open')

    events = events.order_by(Event.date, Event.start_time).all()

    return render_template('index.html', events=events, categories=categories, selected=selected)


@mainbp.route('/search')
def search():
    if request.args.get('search', '').strip() == '':
        return redirect(url_for('main.index'))

    search = request.args['search'].strip()
    query = '%' + search + '%'
    events = Event.query.filter(db.or_(Event.title.like(query), Event.description.like(query))) \
        .order_by(Event.date).all()

    categories = Category.query.order_by(Category.name).all()
    return render_template('index.html', events=events, categories=categories, search=search)


@mainbp.route('/traditional-custodians')
def custodians():
    return render_template('traditional-custodians.html')


@mainbp.route('/bookings')
@login_required
def bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booked_at.desc()).all()
    return render_template('bookings.html', bookings=bookings)


@mainbp.route('/bookings/<int:id>')
@login_required
def booking(id):
    booking = db.get_or_404(Booking, id)

    # people can only see their own bookings
    if booking.user_id != current_user.id:
        abort(404)

    return render_template('booking-confirmation.html', booking=booking)
