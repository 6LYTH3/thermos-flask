import os
from logging import DEBUG
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.logger.setLevel(DEBUG)
app.config['SECRET_KEY'] = 'Z\x02\x99\x91Z\x16\xf9\xdf$\xd2Q\x1a\xfc\x1f\x0f=m'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'\
                                        + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

import models
import views
