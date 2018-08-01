""" Configuration and App Factory """
import sqlite3
from flask import (
    Flask, request, session, g, redirect, url_for, abort, \
    abort, render_template, flash, jsonify
)


DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    """ Connects to the database. """
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    """ Create the Database """
    with app.app_context():
        the_db = get_db()
        with app.open_resource('schema.sql', mode='r') as db_file:
            the_db.cursor().executescript(db_file.read())
        the_db.commit()


def get_db():
    """ Open database connection """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """ Close database connection """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



if '__name__' == '__main__':
    init_db()   
    app.run()

