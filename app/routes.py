from app import app
from flask import jsonify, render_template
from models.season import Season


@app.route('/')
@app.route('/index')
def root():
    return render_template('index.html')


@app.route("/seasons", methods=['GET'])
def season():
    return render_template('seasons.html', seasons=Season.all())
