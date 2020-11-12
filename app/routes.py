from app import app
from flask import jsonify, render_template
from models.season import Season


@app.route('/')
@app.route('/index')
def root():
    return render_template('index.html')


@app.route("/seasons", methods=['GET'])
def season():
    # return jsonify(Season.get(1949)._asdict())
    return render_template('seasons.html', season=Season.get(1949))
