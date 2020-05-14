import os
class Config:
    # going to create the environ with secret key and
    # other info to make it private on server

    # SECRET_KEY = os.environ.get('SECRET_KEY')  # a66cbf4a767c6fd72e6d872a565c8113
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')   # sqlite:///site.db
    SECRET_KEY = 'a66cbf4a767c6fd72e6d872a565c8113'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('my_email')  # google set up 
    MAIL_PASSWORD = os.environ.get('my_password') # googlw app key 