from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO
from book_swapper.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    from book_swapper.users.routes import users
    from book_swapper.books.routes import books
    from book_swapper.main.routes import main
    from book_swapper.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(books)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app