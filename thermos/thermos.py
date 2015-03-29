import os
from datetime import datetime
from logging import DEBUG

from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from forms import BookmarkForm

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.logger.setLevel(DEBUG)
app.config['SECRET_KEY'] = 'Z\x02\x99\x91Z\x16\xf9\xdf$\xd2Q\x1a\xfc\x1f\x0f=m'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
db = SQLAlchemy(app)

import models


def logged_in_user():
    return models.User.query.filter_by(username='xarisd').first()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           new_bookmarks=models.Bookmark.newest(5))


@app.route('/add', methods=['GET', 'POST'])
def add_bookmark():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        # store_bookmark(url, description)
        bm = models.Bookmark(user=logged_in_user(),
                             url=url,
                             description=description)
        db.session.add(bm)
        db.session.commit()
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

# User `python manage.py runserver` to start the server
# if __name__ == '__main__':
#     app.run(debug=True)
