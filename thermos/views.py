from flask import render_template

from thermos import app, login_manager
from models import User, Bookmark, Tag


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           new_bookmarks=Bookmark.newest(5))


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.context_processor
def inject_tags():
    return dict(
        all_tags=Tag.all
    )
