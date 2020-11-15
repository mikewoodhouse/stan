from app import app
from flask import render_template
from models.season import Season
from models.season_record import SeasonRecord


@app.route('/')
@app.route('/index')
def root():
    return render_template('index.html')


@app.route("/seasons", methods=['GET'])
def season():
    return render_template('seasons.html', seasons=Season.all())


@app.route("/season_record/<year>")
def season_record(year):
    recs = SeasonRecord.get(year)
    has_balls = any(r.has_balls for r in recs)
    return render_template('season_record.html', year=year, recs=recs, has_balls=has_balls)
