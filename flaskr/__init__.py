from flask import Flask, request, jsonify
from models.season import Season


app = Flask(__name__,
            static_folder='../static',
            static_url_path='')


@app.route('/')
def root():
    print('**** IN root()) ****')
    return app.send_static_file('index.html')


@app.route("/seasons", methods=['GET'])
def season():
    print(request)
    return jsonify(Season.get(1949)._asdict())
