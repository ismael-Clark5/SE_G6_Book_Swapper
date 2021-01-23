from flask import Flask, escape, request, render_template, url_for

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)