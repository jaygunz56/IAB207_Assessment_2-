from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, Category
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
