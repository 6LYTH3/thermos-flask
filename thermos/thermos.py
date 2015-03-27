from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash
from logging import DEBUG

from forms import BookmarkForm

app = Flask(__name__)
app.logger.setLevel(DEBUG)

app.config['SECRET_KEY'] = 'Z\x02\x99\x91Z\x16\xf9\xdf$\xd2Q\x1a\xfc\x1f\x0f=m'
bookmarks = []


def store_bookmark(url, description):
    bookmarks.append(dict(
        url=url,
        description=description,
        user="xarisd",
        date=datetime.utcnow()
    ))


def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           new_bookmarks=new_bookmarks(5))


@app.route('/add', methods=['GET', 'POST'])
def add_bookmark():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        store_bookmark(url, description)
        flash("Stored bookmark {}".format(description))
        app.logger.debug('store url: ' + url)
        return redirect(url_for('index'))
    return render_template('add.html', form=form)
    # if request.method == "POST":
    #     url = request.form['url']
    #     store_bookmark(url)
    #     flash("Stored bookmark {}".format(url))
    #     app.logger.debug('store url: ' + url)
    #     return redirect(url_for('index'))
    # return render_template('add.html')


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
