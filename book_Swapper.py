from datetime import datetime
from flask import Flask, escape, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

#DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
#app.config['SECRET_KEY'] = '1cd0a8b6b560d0454d1fb43d58ba2bd1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primaryKey = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpeg')
    password = db.Column(db.String(600), nullable = False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"

class Post(db.Model):
    id = db.Column(db.Integer, primaryKey = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
posts = [
    {
        'author': 'Ismael Clark',
        'title': 'First Book',
        'content': 'First book',
        'date_posted': 'January 21 2021'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts = posts)


@app.route('/about')
def about():
    return render_template('about.html', title = 'About the app')


@app.route("/register", methods= ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form = form )


@app.route('/login', methods= ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash('Successfully logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, try again', 'danger')
    return render_template('login.html', title='Login', form = form )


if __name__ == '__main__':
    app.run(debug=True)