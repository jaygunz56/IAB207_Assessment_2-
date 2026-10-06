from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.secret_key = 'triumphmotorevents'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///triumph.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    # send people here if they hit a page that needs a login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    # need to import models here so the tables get created
    from . import models

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, int(user_id))

    with app.app_context():
        db.create_all()
        add_categories()

    from . import views
    app.register_blueprint(views.mainbp)

    from . import auth
    app.register_blueprint(auth.authbp)

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
