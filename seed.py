# Adds some sample events so the site isn't empty while testing.
# Run with: python seed.py
from datetime import date, time, timedelta
from werkzeug.security import generate_password_hash

from website import create_app, db
from website.models import User, Category, Venue, Event, TicketType

app = create_app()

with app.app_context():
    if Event.query.first():
        print('Database already has events, skipping')
        exit()

    organiser = User(first_name='Demo', last_name='Organiser', email='demo@triumph.com',
                     mobile='0400 000 000', password_hash=generate_password_hash('password123'))
    db.session.add(organiser)

    def category(name):
        return Category.query.filter_by(name=name).first()

    today = date.today()

    events = [
        ('Queensland Drift Championship', 'Drifting', 'Queensland Raceway', 'Champions Way, Willowbank QLD',
         'Full-day drifting competition featuring drivers from across Queensland.',
         'img/event-drift.jpg', 11, time(10), time(18), 'Open', 35),
        ('Lakeside Touring Car Weekend', 'Circuit Racing', 'Lakeside Raceway', 'Raceway Rd, Kurwongbah QLD',
         'A weekend of touring car racing with multiple classes competing throughout the day.',
         'img/event-circuit.jpg', 33, time(9), time(17), 'Sold Out', 45),
        ('Sunshine Coast Rally Sprint', 'Rally', 'Sunshine Coast Hinterland', 'Kenilworth QLD',
         'Gravel rally stages through the Sunshine Coast hinterland.',
         'img/event-rally.jpg', 47, time(8), time(16), 'Cancelled', 25),
        ('Spring Motocross Challenge', 'Motocross', 'Toowoomba Motocross Club', 'Wellcamp QLD',
         'Club motocross racing across junior and senior competition classes.',
         'img/event-motocross.jpg', 20, time(8, 30), time(15, 30), 'Open', 20),
    ]

    for title, cat, venue_name, address, desc, image, days, start, end, status, price in events:
        venue = Venue(name=venue_name, address=address)
        event = Event(title=title, description=desc, image=image,
                      date=today + timedelta(days=days), start_time=start, end_time=end,
                      status=status, creator=organiser, category=category(cat), venue=venue)
        event.ticket_types.append(TicketType(name='Spectator', price=price,
                                             quantity_available=0 if status == 'Sold Out' else 200))
        db.session.add(event)

    db.session.commit()
    print('Added sample events')
