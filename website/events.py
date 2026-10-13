import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from .models import Event, Category, Venue, TicketType
from .forms import EventForm
from . import db

eventbp = Blueprint('event', __name__, url_prefix='/events')


@eventbp.route('/<int:id>')
def show(id):
    event = db.get_or_404(Event, id)
    return render_template('event.html', event=event)


@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]

    if form.validate_on_submit():
        image_path = check_upload_file(form)

        # reuse the venue if it's already been added before
        venue = Venue.query.filter_by(name=form.venue_name.data, address=form.venue_address.data).first()
        if venue is None:
            venue = Venue(name=form.venue_name.data, address=form.venue_address.data)

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
                      venue=venue,
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


def check_upload_file(form):
    fp = form.image.data
    # put the time on the front so two images with the same name don't overwrite each other
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + '_' + secure_filename(fp.filename)

    BASE_PATH = os.path.dirname(__file__)
    upload_folder = os.path.join(BASE_PATH, 'static', 'img', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    fp.save(os.path.join(upload_folder, filename))
    return 'img/uploads/' + filename
