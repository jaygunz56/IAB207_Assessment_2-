import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from .models import Event, Category, Venue, TicketType, Comment, Booking
from .forms import EventForm, EditEventForm, CommentForm, BookingForm
from . import db

eventbp = Blueprint('event', __name__, url_prefix='/events')


@eventbp.route('/<int:id>')
def show(id):
    event = db.get_or_404(Event, id)

    booking_form = BookingForm()
    booking_form.ticket_type.choices = [(t.id, t.name) for t in event.ticket_types]
    comment_form = CommentForm()

    return render_template('event.html', event=event, booking_form=booking_form, comment_form=comment_form)


@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]

    if form.validate_on_submit():
        image_path = check_upload_file(form)

        event = Event(title=form.title.data,
                      description=form.description.data,
                      image=image_path,
                      date=form.date.data,
                      start_time=form.start_time.data,
                      end_time=form.end_time.data,
                      parking_info=form.parking_info.data,
                      age_restriction=form.age_restriction.data,
                      spectator_access=form.spectator_access.data,
                      acknowledgement=form.acknowledgement.data,
                      category_id=form.category.data,
                      venue=get_venue(form),
                      creator=current_user)

        ticket = TicketType(name=form.ticket_type.data,
                            price=form.ticket_price.data,
                            quantity_available=form.ticket_quantity.data,
                            event=event)

        db.session.add(event)
        db.session.add(ticket)
        db.session.commit()

        flash('Your event has been created', 'success')
        return redirect(url_for('event.show', id=event.id))

    return render_template('create-event.html', form=form)


@eventbp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    event = db.get_or_404(Event, id)

    # only the person who made the event can change it
    if event.user_id != current_user.id:
        abort(403)

    if event.status == 'Cancelled':
        flash("Cancelled events can't be edited", 'warning')
        return redirect(url_for('event.show', id=event.id))

    form = EditEventForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    ticket = event.ticket_types[0]

    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.parking_info = form.parking_info.data
        event.age_restriction = form.age_restriction.data
        event.spectator_access = form.spectator_access.data
        event.acknowledgement = form.acknowledgement.data
        event.category_id = form.category.data
        event.venue = get_venue(form)

        # keep the old image unless a new one was picked
        if form.image.data:
            event.image = check_upload_file(form)

        ticket.name = form.ticket_type.data
        ticket.price = form.ticket_price.data
        ticket.quantity_available = form.ticket_quantity.data

        # might be sold out or open again depending on the new ticket numbers
        event.update_status()

        db.session.commit()
        flash('Your event has been updated', 'success')
        return redirect(url_for('event.show', id=event.id))

    if request.method == 'GET':
        form.title.data = event.title
        form.category.data = event.category_id
        form.description.data = event.description
        form.date.data = event.date
        form.start_time.data = event.start_time
        form.end_time.data = event.end_time
        form.venue_name.data = event.venue.name
        form.venue_address.data = event.venue.address
        form.parking_info.data = event.parking_info
        form.ticket_type.data = ticket.name
        form.ticket_price.data = ticket.price
        form.ticket_quantity.data = ticket.quantity_available
        form.age_restriction.data = event.age_restriction
        form.acknowledgement.data = event.acknowledgement
        form.spectator_access.data = event.spectator_access

    return render_template('create-event.html', form=form, event=event)


@eventbp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    event = db.get_or_404(Event, id)

    if event.user_id != current_user.id:
        abort(403)

    event.status = 'Cancelled'
    db.session.commit()

    flash('Your event has been cancelled', 'info')
    return redirect(url_for('event.show', id=event.id))


@eventbp.route('/<int:id>/comment', methods=['POST'])
@login_required
def comment(id):
    event = db.get_or_404(Event, id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(text=form.text.data, user=current_user, event=event)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted', 'success')
    else:
        flash('Comments need some text and can be up to 400 characters', 'danger')

    return redirect(url_for('event.show', id=event.id) + '#comments')


@eventbp.route('/<int:id>/book', methods=['POST'])
@login_required
def book(id):
    event = db.get_or_404(Event, id)

    if event.status != 'Open':
        flash("Sorry, this event isn't taking bookings", 'danger')
        return redirect(url_for('event.show', id=event.id))

    form = BookingForm()
    form.ticket_type.choices = [(t.id, t.name) for t in event.ticket_types]

    if form.validate_on_submit():
        ticket = db.session.get(TicketType, form.ticket_type.data)

        if form.quantity.data > ticket.quantity_available:
            flash(f'Sorry, there are only {ticket.quantity_available} tickets left', 'danger')
            return redirect(url_for('event.show', id=event.id))

        booking = Booking(quantity=form.quantity.data,
                          total_price=round(ticket.price * form.quantity.data, 2),
                          user=current_user,
                          event=event,
                          ticket_type=ticket)
        ticket.quantity_available = ticket.quantity_available - form.quantity.data
        event.update_status()

        db.session.add(booking)
        db.session.commit()

        flash('Booking confirmed!', 'success')
        return redirect(url_for('main.booking', id=booking.id))
    else:
        flash('Please pick a ticket type and between 1 and 5 tickets', 'danger')

    return redirect(url_for('event.show', id=event.id))


def get_venue(form):
    # reuse the venue if it's already been added before
    venue = Venue.query.filter_by(name=form.venue_name.data, address=form.venue_address.data).first()
    if venue is None:
        venue = Venue(name=form.venue_name.data, address=form.venue_address.data)
    return venue


def check_upload_file(form):
    fp = form.image.data
    # put the time on the front so two images with the same name don't overwrite each other
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + '_' + secure_filename(fp.filename)

    BASE_PATH = os.path.dirname(__file__)
    upload_folder = os.path.join(BASE_PATH, 'static', 'img', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    fp.save(os.path.join(upload_folder, filename))
    return 'img/uploads/' + filename
