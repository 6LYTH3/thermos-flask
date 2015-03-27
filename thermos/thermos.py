from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from logging import DEBUG

app = Flask(__name__)
app.logger.setLevel(DEBUG)

app.config['SECRET_KEY'] = 'Z\x02\x99\x91Z\x16\xf9\xdf$\xd2Q\x1a\xfc\x1f\x0f=m'
bookmarks = []


def store_bookmark(url):
    bookmarks.append(dict(
        url=url,
        user="xarisd",
        date=datetime.utcnow()
    ))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Title passed from view to template',
                           user=User('Haris', 'Dimitriou'))


@app.route('/add', methods=['GET', 'POST'])
def add_bookmark():
    if request.method == "POST":
        url = request.form['url']
        store_bookmark(url)
        flash("Stored bookmark {}".format(url))
        app.logger.debug('store url: ' + url)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def initials(self):
        return "{}. {}".format(self.firstname[0], self.lastname[0])

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)


if __name__ == '__main__':
    app.run(debug=True)
