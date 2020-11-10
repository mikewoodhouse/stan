from flask import Flask
from models.season import Season


app = Flask(__name__)


@app.route("/season")
def season():
    return str(Season.get(1949))
