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


@app.route('/players')
def players():
    conn = sqlite3.connect('tocc.sqlite')
    conn.row_factory = namedtuple_factory
    csr = conn.cursor()
    data = csr.execute("""
    SELECT
      p.code
    , p.surname || ', ' || IfNull(p.firstname, IfNull(p.initial, '?')) name
    , Min(f.year) from_year
    , Max(f.year) to_year
    , Sum(matches) matches
    FROM players p
    , performances f
    WHERE p.code = f.code
    GROUP BY p.code
    , p.surname || ', ' || IfNull(p.firstname, IfNull(p.initial, '?'))
    ORDER BY p.surname || ', ' || IfNull(p.firstname, IfNull(p.initial, '?'))
    """).fetchall()
    csr.close()
    conn.close()
    return render_template('players.html', data=data)


@app.route('/player/<code>')
def player(code):
    print(f'{code=}')
    player = {'name': 'Bonzo Dogdoodah' + f'({code})'}
    conn = sqlite3.connect('tocc.sqlite')
    conn.row_factory = namedtuple_factory
    csr = conn.cursor()
    player = csr.execute("""
    SELECT p.surname || ', ' || IfNull(p.firstname, IfNull(p.initial, '?')) name
    FROM players p
    WHERE code = ?
    """, (code,)).fetchone()
    csr.close()
    csr = conn.cursor()
    data = csr.execute("""
    SELECT
      *
    , CASE highest_not_out
        WHEN 1 THEN '*'
        ELSE ''
      END high_not_out_flag
    , CASE innings
        WHEN 0 THEN 0.0
        ELSE
            CASE not_out
                WHEN innings THEN 0.0
                ELSE Round(Cast(runs_scored AS REAL) / (Cast(innings - not_out AS REAL)), 2)
            END
        END bat_ave
    , CASE wickets
        WHEN 0 THEN 0
        ELSE Cast(runs_conceded AS REAL) / Cast(wickets AS REAL)
    END bowl_ave
    FROM performances
    WHERE code = ?
    ORDER BY year
    """, (code,)).fetchall()
    csr.close()
    conn.close()
    print(data[0])
    return render_template('player.html', player=player, data=data)


if __name__ == "__main__":
    app.run()
