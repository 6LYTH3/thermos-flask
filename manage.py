#! /usr/bin/env python

from thermos import app, db
from thermos.models import User
from flask.ext.script import Manager, prompt_bool

manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username='xarisd', email='xaris.dimitriou@gmail.com'))
    db.session.add(User(username='matinabla', email='matinabla@yahoo.gr'))
    db.session.commit()
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you wamt to lloase all your data?"):
        db.drop_all()
        print("Dropped the database")


if __name__ == "__main__":
    manager.run()
