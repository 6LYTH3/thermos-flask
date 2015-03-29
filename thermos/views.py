from flask import render_template, redirect, url_for, flash
# from datetime import datetime

from thermos import app, db
from forms import BookmarkForm
from models import User, Bookmark


# Fake login
def logged_in_user():
    return User.query.filter_by(username='xarisd').first()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           new_bookmarks=Bookmark.newest(5))


@app.route('/add', methods=['GET', 'POST'])
def add_bookmark():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user=logged_in_user(),
                      url=url,
                      description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored {}".format(description))
        app.logger.debug('store url: ' + url)
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
