#! /usr/bin/env python

from thermos import app, db
from thermos.models import User, Bookmark, Tag
from flask.ext.script import Manager, prompt_bool
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def insert_data():
    # Add users
    xarisd = User(username='xarisd',
                  email='xaris.dimitriou@gmail.com',
                  password='123'
                  )

    db.session.add(xarisd)

    matina = User(username='matinabla',
                  email='matinabla@yahoo.gr',
                  password='123'
                  )
    db.session.add(matina)

    db.session.commit()

    # Add tags
    for name in ["python", "flask", "webdev", "views", "forms", "html5", ]:
        db.session.add(Tag(name=name))
    db.session.commit()

    def add_bookmark(url, description, tags):
        db.session.add(Bookmark(url=url,
                                description=description,
                                tags=tags,
                                user=xarisd
                                )
                       )

    add_bookmark('http://flask.pocoo.org/', 'Flask', 'flask,python')
    add_bookmark('http://jinja.pocoo.org/', 'Jinja2', 'flask,python,views')
    add_bookmark('http://www.initializr.com', 'Initializr', 'html5,webdev')
    add_bookmark('http://flask.pocoo.org/docs/0.10/quickstart/#url-building',
                 'Url building in Flask', 'html5,webdev,flask,python')
    add_bookmark('https://pypi.python.org/pypi/Flask-Bootstrap',
                 'Flask-Bootstrap extension', 'html5,webdev,flask,python')
    add_bookmark('http://jinja.pocoo.org/docs/dev/templates/'
                 '#list-of-control-structures',
                 'Control structures in Jinja2', 'flask,python,views')
    add_bookmark('https://flask-wtf.readthedocs.org/en/latest/',
                 'Flask-WTF documentation', 'python,flask,html5,webdev,forms')

    db.session.commit()
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you wamt to lloase all your data?"):
        db.drop_all()
        print("Dropped the database")


if __name__ == "__main__":
    manager.run()
