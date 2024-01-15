from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from . import models

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.selectUserType'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userId):
        student = models.Student.query.get(userId)
        admin = models.Admin.query.get(userId)

        if student:
            return student
        elif admin:
            return admin
        else:
            return None

    return app

def create_database(app):
    with app.app_context():
        db.create_all()