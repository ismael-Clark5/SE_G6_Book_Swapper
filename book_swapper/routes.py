import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from book_swapper import app, bcrypt, db, mail
from book_swapper.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                NewBookForm, RequestResetForm, ResetPasswordForm)
from book_swapper.models import User, Book
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.date_posted.desc()).paginate(page = page, per_page=4)
    return render_template('home.html', books=books)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created. You can now log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect (url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods =["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file = image_file, form = form)


@app.route("/book/new", methods=['GET', 'POST'])
@login_required
def post_book():
    form = NewBookForm()
    if form.validate_on_submit():
        book = Book(title = form.title.data, subject = form.subject.data,isbn=form.isbn.data,
                    subject_subcategory =form.subject_subcategory.data, condition = form.condition.data,
                    date_posted = form.date_posted.data, owner=current_user)
        db.session.add(book)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('post_book.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/book/<int:book_id>")
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, book=book)


@app.route("/book/<int:book_id>/update", methods=['GET', 'POST'])
@login_required
def update_book_post(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner !=current_user:
        abort(403)
    form = NewBookForm()
    if form.validate_on_submit():
        book.title= form.title.data
        book.condition= form.condition.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('book', book_id = book.id))
    elif request.method == 'GET':
        form.title.data= book.title
        form.condition.data = book.condition
    return render_template('post_book.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/book/<int:book_id>/delete_book", methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner != current_user:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_books(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    books = Book.query.filter_by(owner=user)\
        .order_by(Book.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('user_books.html', books=books, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password Reset Request',
                  sender ='ismaclark98@gmail.com',
                  recipients=[user.email])
    message.body = f'''To reset your password visit the following link:
{url_for('reset_token', token=[token], _external=True)}

If you did not make this request simply ignore this email  
'''
    mail.send(message)


@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)



@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user=user.verifiy_reset_token(token)
    if user is None:
        flash('That is an invalid token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated. You can now log in!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)