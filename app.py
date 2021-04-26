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


if __name__ == "__main__":
    app.run()
