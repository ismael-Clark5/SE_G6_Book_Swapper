from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from book_swapper import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    school = db.Column(db.String(60), nullable = True)
    city = db.Column(db.String(60), nullable = True)
    books = db.relationship('Book', backref='owner', lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        s.dumps( {"user_id": self.id} ).decode('utf-8')


    @staticmethod
    def verifiy_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(30), nullable = False)
    isbn = db.Column(db.String(15), nullable=False)
    subject_subcategory = db.Column(db.String(30), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    condition = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
