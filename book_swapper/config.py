import os

class Config:
    #SECRET_KEY=os.environ.get('SECRET_KEY')
    SECRET_KEY = '701d2f2232bf1eb1d2d4dfd3b052d447' #delete, hard code
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # delete, hard code
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = 'True'
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
