import models

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

# ROUTES:
# GET - http://localhost:8000/api/v1/recipes/
# POST - http://localhost:8000/api/v1/recipes/
# GET - http://localhost:8000/api/v1/recipes/1


# first argument is the blueprints name
# second argument is the import_name
# third arguement is the url_prefix so we don't have to prefix all of our apis with /api/v1
recipe = Blueprint('recipes', 'recipe')


@recipe.route('/', methods=['GET'])
@login_required
def get_all_recipes():
  # if not current_user.email.endswith('.edu'):
  #   return jsonify(data={}, status={'code': 403, 'message': 'Not authorized'})

  try:
    recipes = [model_to_dict(recipe) for recipe in current_user.recipes]

    return jsonify(data=recipes, status={'code': 200, 'message': 'Success'})
  except models.DoesNotExist:
    return jsonify(data={}, status={'code': 401, 'message' :'Error getting the resources'})


@recipe.route('/', methods=['POST'])
@login_required
def create_recipes():
  payload = request.get_json()

  recipe = models.Recipe.create(name=payload['name'], owner=current_user.id, image=payload['image'], servings=payload['servings'], ingredientOne=payload['ingredientOne'], ingredientTwo=payload['ingredientTwo'], ingredientThree=payload['ingredientThree'], ingredientFour=payload['ingredientFour'], ingredientFive=payload['ingredientFive'], ingredientSix=payload['ingredientSix'], ingredientSeven=payload['ingredientSeven'], ingredientEight=payload['ingredientEight'], ingredientNine=payload['ingredientNine'], ingredientTen=payload['ingredientTen'], notes=payload['notes'])

  recipe_dict = model_to_dict(recipe)

  return jsonify(data=recipe_dict, status={"code": 201, "message": "Successful recipe creation"})


@recipe.route('/<recipe_id>', methods=['GET'])
@login_required
def get_one_recipe(recipe_id):
  """
  - We have a route param that is the ID we want to search
  - Search PSQL for that ID
    - What do we do when the database doesn't have the id?
  - Return that value in the response
  """
  print(f'Searching for recipe_id: {recipe_id}')
  try:
    recipe = models.Recipe.get_by_id(recipe_id)

    return jsonify(data=model_to_dict(recipe), status={'code': 200, 'message': 'Success'})
  except models.DoesNotExist:
    return jsonify(data={}, status={'code': 404, 'message' : f'Recipe resource {recipe_id} does not exist'})


"""
curl \
-X PUT \
-H "Content-Type: application/json" \
-d '{"name": "Sidney", "breed":"Labradoodle", "owner":"Tina Winchester"}' \
'http://localhost:8000/api/v1/recipes/1'
"""
@recipe.route('/<recipe_id>', methods=['PUT'])
@login_required
def update_recipe(recipe_id):
  payload = request.get_json()

  query = models.Recipe.update(**payload).where(models.Recipe.id == recipe_id)
  
  try:
    query.execute()

    recipe = models.Recipe.get_by_id(recipe_id)

    return jsonify(data=model_to_dict(recipe), status={'code': 200, 'message': 'Success'})
  except models.DoesNotExist:
    return jsonify(data={}, status={'code': 404, 'message' : f'Recipe resource {recipe_id} does not exist'})


"""
curl -X DELETE 'http://localhost:8000/api/v1/recipes/3'
"""
@recipe.route('/<recipe_id>', methods=['DELETE'])
@login_required
def delete_recipe(recipe_id):
  query = models.Recipe.delete().where(models.Recipe.id == recipe_id)
  del_rows = query.execute()
  # del_rows = models.Recipe.delete_by_id(recipe_id)

  print(f'deleted rows: {del_rows}')

  # 0 is a falsy value. If del_rows is anything other than 0 we know the operation worked
  if del_rows:
    return jsonify(data=f'Deleted {del_rows} successfully', status={'code': 200, 'message':'resource successfully deleted'})
  else:
    return jsonify(data='No resource to delete', status={'code': 404, 'message': f'Recipe resource {recipe_id} does not exist'})

