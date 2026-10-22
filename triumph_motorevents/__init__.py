import os
from datetime import date
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_bootstrap import Bootstrap5

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # set SECRET_KEY on the server, the random key is only a fallback for running locally
    app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///triumph.sqlite'

    db.init_app(app)
    # checks the csrf token on every form post, not just the wtforms ones
    CSRFProtect(app)
    Bootstrap5(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # need to import models here so the tables get created
    from . import models

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(models.User).where(models.User.id == user_id))

    with app.app_context():
        db.create_all()
        add_categories()

    @app.before_request
    def check_finished_events():
        # anything that's already finished gets marked as inactive
        if request.endpoint == 'static':
            return

        from .models import Event
        events = Event.query.filter(Event.status.in_(['Open', 'Sold Out']), Event.date <= date.today()).all()
        for event in events:
            event.update_status()
        db.session.commit()

    @app.template_filter('nicedate')
    def nicedate(value):
        return value.strftime('%d %B %Y').lstrip('0')

    @app.template_filter('nicetime')
    def nicetime(value):
        return value.strftime('%I:%M %p').lstrip('0')

    @app.errorhandler(CSRFError)
    def csrf_error(e):
        return render_template('error.html', code=400, title='Your session expired',
                               message='Please go back, refresh the page and try that again.'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error.html', code=403, title="You can't do that",
                               message="You don't have permission to view or change this page."), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('error.html', code=404, title='Page not found',
                               message="We couldn't find what you were looking for. It might have been moved or never existed."), 404

    @app.errorhandler(500)
    def server_error(e):
        # rollback in case something was half saved
        db.session.rollback()
        return render_template('error.html', code=500, title='Something went wrong',
                               message="That one's on us. Please try again in a minute."), 500

    from . import views
    app.register_blueprint(views.mainbp)

    from . import auth
    app.register_blueprint(auth.authbp)

    from . import events
    app.register_blueprint(events.eventbp)

    return app


def add_categories():
    # categories are fixed so just make sure they're in the db
    from .models import Category
    names = ['Circuit Racing', 'Drifting', 'Drag Racing', 'Rally',
             'Motocross', 'Track Day', 'Motorsport Festival']
    if Category.query.count() == 0:
        for name in names:
            db.session.add(Category(name=name))
        db.session.commit()
