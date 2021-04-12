from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager

import models
from resources.users import user
from resources.recipes import recipe


DEBUG = True
# 8000 or 5000 are the common python web server ports
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = 'TOPSECRETDONOTSTEAL'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.RecipeUser.get(models.RecipeUser.id == user_id)
    except:
        print(f'User not found: {user_id}')
        return None


@app.before_request
def before_request():
    """
    Connect to the database before each request
    """
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """
    Close the database connection after each request
    """
    g.db.close()
    return response


CORS(recipe, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(recipe, url_prefix='/api/v1/recipes')

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/users')


@app.route('/')
def index():
    my_list = ['Fancy', 'Flask', 'application']
    # return jsonify(my_list)
    return jsonify(name='Phil', fav_language='Python')


@app.route('/test')
def test():
    return jsonify('test')


@app.route('/sayhi/<name>')
def hello(name):
    return f'Hello {name}'
    # return f'Hello {}'.format(name)


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
