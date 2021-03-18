from flask import Blueprint, render_template, request
from book_swapper.models import Book

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.date_posted.desc()).paginate(page = page, per_page=4)
    return render_template('home.html', books=books)


@main.route("/about")
def about():
    return render_template('about.html', title='About')