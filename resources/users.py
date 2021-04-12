import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

# first argument is the blueprints name
# second argument is the import_name
# third arguement is the url_prefix so we don't have to prefix all of our apis with /api/v1
user = Blueprint('users', 'user')


@user.route('/', methods=['GET'])
def get_users():
    return 'here is a user'


"""
curl \
-X POST \
-H "Content-Type: application/json" \
-d '{"username": "test", "email": "test@example.com", "password": "test"}' \
'http://localhost:8000/api/v1/users/register'
"""
@user.route('/register', methods=['POST'])
def register():
    payload = request.get_json()

    payload['email'] = payload['email'].lower()

    try:
        models.RecipeUser.get(models.RecipeUser.email == payload['email'])
        return jsonify(data={}, status={'code': 401, 'message': 'A user with that email already exists'})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.RecipeUser.create(**payload)

        login_user(user)

        user_dict = model_to_dict(user)
        del user_dict['password']

        return jsonify(data=user_dict, status={'code': 201, 'message': 'Successfully created a user'})


"""
curl \
-X POST \
-H "Content-Type: application/json" \
-d '{"username": "test", "email": "test@example.com", "password": "test"}' \
'http://localhost:8000/api/v1/users/login'
"""
@user.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()

    try:
        user = models.RecipeUser.get(models.RecipeUser.email == payload['email'])
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Email does not exist'})


    if user:
        user_dict = model_to_dict(user)

        if (check_password_hash(user_dict['password'], payload['password'])):
            login_user(user)
            del user_dict['password']

            return jsonify(data=user_dict, status={'code': 200, 'message': 'Login Successful'})
        else:
            return jsonify(data={}, status={'code': 401, 'message': 'Incorrect username or pasword'})

@user.route('/logout', methods=['GET'])
def logout():
    logout_user() # this has a lot of logout functionality for us
    return jsonify(data={}, status={'code': 200, 'message': 'successful logout'})
