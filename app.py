from flask import Flask
from flask import render_template

import sqlite3
from collections import namedtuple


def namedtuple_factory(cursor, row):
    """
    Usage:
    con.row_factory = namedtuple_factory
    """
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates',
            static_url_path='')


@app.route('/')
@app.route('/index')
def root():
    return render_template('index.html')


@app.route('/seasons')
def seasons():
    conn = sqlite3.connect('tocc.sqlite')
    conn.row_factory = namedtuple_factory
    csr = conn.cursor()
    data = csr.execute('SELECT * FROM seasons ORDER BY year').fetchall()
    csr.close()
    conn.close()
    return render_template('seasons.html', data=data)


if __name__ == "__main__":
    app.run()
