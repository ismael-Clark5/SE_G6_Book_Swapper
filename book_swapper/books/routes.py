from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from book_swapper import db
from book_swapper.models import Book
from book_swapper.books.forms import NewBookForm

books = Blueprint('books', __name__)

@books.route("/book/new", methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))
    return render_template('post_book.html', title='New Post',
                           form=form, legend='New Post')


@books.route("/book/<int:book_id>")
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, book=book)


@books.route("/book/<int:book_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('books.book', book_id = book.id))
    elif request.method == 'GET':
        form.title.data= book.title
        form.condition.data = book.condition
    return render_template('post_book.html', title='Update Post',
                           form=form, legend='Update Post')


@books.route("/book/<int:book_id>/delete_book", methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.owner != current_user:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
