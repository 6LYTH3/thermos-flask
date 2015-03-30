import os
from logging import DEBUG
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.moment import Moment
from flask_debugtoolbar import DebugToolbarExtension


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Configure database
app.logger.setLevel(DEBUG)
app.config['SECRET_KEY'] = 'Z\x02\x99\x91Z\x16\xf9\xdf$\xd2Q\x1a\xfc\x1f\x0f=m'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'\
                                        + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = "auth.login"
login_manager.init_app(app)

# Enable debugtoolbar
toolbar = DebugToolbarExtension(app)

# for displaying timestamps
moment = Moment(app)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

import models
import views
