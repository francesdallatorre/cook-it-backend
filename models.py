import os
from peewee import *
# from peewee import PostgresqlDatabase, CharField, DateTimeField, Model
from datetime import datetime
from flask_login import UserMixin

# you have to manually create the database yourself.
# `createdb recipes` in your terminal
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))

else: 
    DATABASE = PostgresqlDatabase('recipes')
 




class RecipeUser(UserMixin, Model):
    # null=True is implicity in all definitions
    username = CharField()
    email = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = DATABASE


# Extend peewee Model class and add our own 
# logic and schema on top of it
# http://docs.peewee-orm.com/en/latest/peewee/models.html#field-initialization-arguments
class Recipe(Model):
    name = CharField()
    owner = ForeignKeyField(RecipeUser, backref='recipes')
    image = CharField()
    servings = CharField()
    ingredientOne = CharField()
    ingredientTwo = CharField()
    ingredientThree = CharField()
    ingredientFour = CharField()
    ingredientFive = CharField()
    ingredientSix = CharField()
    ingredientSeven = CharField()
    ingredientEight = CharField()
    ingredientNine = CharField()
    ingredientTen = CharField()
    notes = CharField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Recipe, RecipeUser], safe=True)
    print('TABLES Created')
    DATABASE.close()
