from datetime import date
from flask import Blueprint, render_template, request
from .models import Event, Category

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
