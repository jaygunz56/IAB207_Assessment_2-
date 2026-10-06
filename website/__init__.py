from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.secret_key = 'triumphmotorevents'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///triumph.sqlite'

    db.init_app(app)

    # need to import models here so the tables get created
    from . import models

    with app.app_context():
        db.create_all()

    from . import views
    app.register_blueprint(views.mainbp)

    return app
