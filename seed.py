# adds a few events so the site has something on it when testing
# run with: python seed.py
from datetime import date, time, timedelta
from werkzeug.security import generate_password_hash

from website import create_app, db
from website.models import User, Category, Venue, Event, TicketType

app = create_app()

with app.app_context():
    if Event.query.first():
        print('Events already added')
        exit()

    user = User(first_name='Demo', last_name='Organiser', email='demo@triumph.com',
                mobile='0400 000 000', password_hash=generate_password_hash('password123'))
    db.session.add(user)

    # dates are worked out from today so the events are always upcoming
    today = date.today()

    event1 = Event(title='Queensland Drift Championship',
                   description='Full-day drifting competition featuring drivers from across Queensland.',
                   image='img/event-drift.jpg',
                   date=today + timedelta(days=11),
                   start_time=time(10, 0),
                   end_time=time(18, 0),
                   status='Open',
                   creator=user,
                   category=Category.query.filter_by(name='Drifting').first(),
                   venue=Venue(name='Queensland Raceway', address='Champions Way, Willowbank QLD'))
    db.session.add(event1)
    db.session.add(TicketType(name='Spectator', price=35, quantity_available=200, event=event1))

    event2 = Event(title='Lakeside Touring Car Weekend',
                   description='A weekend of touring car racing with multiple classes competing throughout the day.',
                   image='img/event-circuit.jpg',
                   date=today + timedelta(days=33),
                   start_time=time(9, 0),
                   end_time=time(17, 0),
                   status='Sold Out',
                   creator=user,
                   category=Category.query.filter_by(name='Circuit Racing').first(),
                   venue=Venue(name='Lakeside Raceway', address='Raceway Rd, Kurwongbah QLD'))
    db.session.add(event2)
    db.session.add(TicketType(name='Spectator', price=45, quantity_available=0, event=event2))

    event3 = Event(title='Sunshine Coast Rally Sprint',
                   description='Gravel rally stages through the Sunshine Coast hinterland.',
                   image='img/event-rally.jpg',
                   date=today + timedelta(days=47),
                   start_time=time(8, 0),
                   end_time=time(16, 0),
                   status='Cancelled',
                   creator=user,
                   category=Category.query.filter_by(name='Rally').first(),
                   venue=Venue(name='Sunshine Coast Hinterland', address='Kenilworth QLD'))
    db.session.add(event3)
    db.session.add(TicketType(name='Spectator', price=25, quantity_available=200, event=event3))

    event4 = Event(title='Spring Motocross Challenge',
                   description='Club motocross racing across junior and senior competition classes.',
                   image='img/event-motocross.jpg',
                   date=today + timedelta(days=20),
                   start_time=time(8, 30),
                   end_time=time(15, 30),
                   status='Open',
                   creator=user,
                   category=Category.query.filter_by(name='Motocross').first(),
                   venue=Venue(name='Toowoomba Motocross Club', address='Wellcamp QLD'))
    db.session.add(event4)
    db.session.add(TicketType(name='Spectator', price=20, quantity_available=200, event=event4))

    db.session.commit()
    print('Added 4 events')
