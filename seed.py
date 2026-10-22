# adds sample events, users, bookings and comments so the site has something on it when testing
# run with: python seed.py
from datetime import date, time, timedelta
from werkzeug.security import generate_password_hash

from website import create_app, db
from website.models import User, Category, Venue, Event, TicketType, Booking, Comment

app = create_app()

with app.app_context():
    if Event.query.first():
        print('Events already added')
        exit()

    user = User(first_name='Demo', last_name='Organiser', email='demo@triumph.com',
                mobile='0400 000 000', street_address='1 George St, Brisbane QLD 4000',
                password_hash=generate_password_hash('password123'))
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

    event5 = Event(title='Willowbank Friday Night Drags',
                   description='Quarter mile drag racing under lights. Street cars, bikes and pro classes all run '
                               'on the night, and the pits are open to spectators between rounds.',
                   image='img/event-circuit.jpg',
                   date=today + timedelta(days=16),
                   start_time=time(17, 0),
                   end_time=time(22, 30),
                   status='Open',
                   age_restriction='All ages',
                   parking_info='Free parking in the main spectator car park off Champions Way.',
                   acknowledgement='generic',
                   creator=user,
                   category=Category.query.filter_by(name='Drag Racing').first(),
                   venue=Venue(name='Willowbank Raceway', address='Champions Way, Willowbank QLD'))
    db.session.add(event5)
    db.session.add(TicketType(name='Spectator', price=30, quantity_available=300, event=event5))

    event6 = Event(title='Morgan Park Open Track Day',
                   description='Bring your own car and get some laps in on a proper circuit. Sessions are split '
                               'into novice, intermediate and advanced groups, with instructors available for '
                               'first timers. Helmet and a roadworthy car are required.',
                   image='img/event-circuit.jpg',
                   date=today + timedelta(days=27),
                   start_time=time(7, 30),
                   end_time=time(16, 30),
                   status='Open',
                   age_restriction='18+',
                   spectator_access=False,
                   parking_info='Trailer parking available in the pit area.',
                   creator=user,
                   category=Category.query.filter_by(name='Track Day').first(),
                   venue=Venue(name='Morgan Park Raceway', address='Morgan Park Rd, Warwick QLD'))
    db.session.add(event6)
    db.session.add(TicketType(name='Participant Entry', price=180, quantity_available=40, event=event6))

    event7 = Event(title='Adelaide Motorsport Festival',
                   description='A weekend celebrating motorsport history in the heart of Adelaide, with historic '
                               'race cars, rally cars and modern supercars on display and on track.',
                   image='img/event-drift.jpg',
                   date=today + timedelta(days=40),
                   start_time=time(9, 0),
                   end_time=time(18, 0),
                   status='Open',
                   acknowledgement='enhanced',
                   traditional_custodians='Kaurna',
                   creator=user,
                   category=Category.query.filter_by(name='Motorsport Festival').first(),
                   venue=Venue(name='Victoria Park', address='Wakefield St, Adelaide SA'))
    db.session.add(event7)
    db.session.add(TicketType(name='Spectator', price=55, quantity_available=500, event=event7))

    # already happened, so it shows as inactive
    event8 = Event(title='Winter Drift Practice Day',
                   description='Open practice session for drift drivers getting ready for the championship.',
                   image='img/event-drift.jpg',
                   date=today - timedelta(days=12),
                   start_time=time(9, 0),
                   end_time=time(15, 0),
                   status='Inactive',
                   creator=user,
                   category=Category.query.filter_by(name='Drifting').first(),
                   venue=Venue(name='Queensland Raceway', address='Champions Way, Willowbank QLD'))
    db.session.add(event8)
    db.session.add(TicketType(name='Spectator', price=15, quantity_available=100, event=event8))

    sarah = User(first_name='Sarah', last_name='Mitchell', email='sarah@example.com',
                 mobile='0412 345 678', street_address='24 Boundary St, West End QLD 4101',
                 password_hash=generate_password_hash('password123'))
    daniel = User(first_name='Daniel', last_name='Reid', email='daniel@example.com',
                  mobile='0423 456 789', street_address='8 Ann St, Ipswich QLD 4305',
                  password_hash=generate_password_hash('password123'))
    db.session.add_all([sarah, daniel])

    # bookings take tickets off what's available, same as booking through the site
    bookings = [(daniel, event1, 2), (sarah, event4, 4), (sarah, event5, 1), (daniel, event5, 3)]
    for person, event, quantity in bookings:
        ticket = event.ticket_types[0]
        db.session.add(Booking(quantity=quantity, total_price=ticket.price * quantity,
                               user=person, event=event, ticket_type=ticket))
        ticket.quantity_available = ticket.quantity_available - quantity

    db.session.add(Comment(text='Went last year and it was a great day. Get there early for a good spot.',
                           user=daniel, event=event1))
    db.session.add(Comment(text='Does anyone know if the spectator parking fills up quickly in the morning?',
                           user=sarah, event=event1))
    db.session.add(Comment(text='Bringing the kids to this one, they loved the juniors racing last time.',
                           user=sarah, event=event4))
    db.session.add(Comment(text='Is there a burnout comp on the night or just drags?',
                           user=daniel, event=event5))

    db.session.commit()
    print('Added 8 events, 3 users, 4 bookings and 4 comments')
