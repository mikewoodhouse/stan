from flask import Flask
from flask import render_template


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
    data = [
        {'year': 1949, 'played': 12, 'won': 4, 'lost': 7, 'drawn': 1, 'tie': 0, 'noresult': 0, 'maxpossiblegames': 12},
        {'year': 1950, 'played': 14, 'won': 6, 'lost': 6, 'drawn': 2, 'tie': 0, 'noresult': 0, 'maxpossiblegames': 14},
    ]
    return render_template('seasons.html', data=data)


if __name__ == "__main__":
    app.run()
