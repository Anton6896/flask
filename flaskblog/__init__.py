""" flask main page 
! do this way is to avoid the circular calls of methods, 
! this is the right way to implement the calls for db, app, etc. 
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # pip install flask-sqlalchemy
from flask_bcrypt import Bcrypt  # pip install flask-bcrypt
from flask_login import LoginManager  # pip install flask-login
from flask_mail import Mail
import os
from flaskblog.config import Config


db = SQLAlchemy()  # db
bcrypt = Bcrypt()  # bcrypt
login_manager = LoginManager()  # flask_login
login_manager.login_view = 'users.login'  # redirect if user not authenticated
login_manager.login_message_category = 'info'  # message constructor -> bootstarp
mail = Mail()


def create_app(config_lass=Config):
    app = Flask(__name__)
    app.config.from_object(Config)  # get config fom class

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from .main.routs import main
    from .posts.routs import posts
    from .users.routs import users
    from .errors.hendlers import errors
    
    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
