import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'breaking_bread_project.settings')
from django.utils.timezone import now
import django
django.setup()
from breakingbread.models import *

def populate():
    Italian_recipes = [
        {'recipe_id': 1, 'recipe_name': 'Bruschetta', 'username': 'johndoe', 'time_taken': 20,
         'level': 0, 'ingredients': 'tomato,garlic,bread', 'cooking_type': 1, 'cuisine': 'Italian',
         'description': 'Mix all :)', 'created': now},
       ]
    Indian_recipes = [{'recipe_id': 2, 'recipe_name': 'Tandoori Chicken', 'username': 'johndoe', 'time_taken': 50,
         'level': 1, 'ingredients': 'chicken, spices, onion', 'cooking_type': 0, 'cuisine': 'Indian',
         'description': 'Cook chicken :)', 'created': now},]
    Egyptian_Recipes = [
        {'recipe_id': 3, 'recipe_name': 'Koshari', 'username': 'johndoe', 'time_taken': 60,
         'level': 1, 'ingredients': 'pasta, lentils, onions, garlic, vinegar, chickpeas, rice, salsa', 'cooking_type': 1, 'cuisine': 'Egyptian',
         'description': 'Mix and fry the onions :)', 'created': now},]

    Scottish_Recipes = [
        {'recipe_id': 4, 'recipe_name': 'Black Pudding', 'username': 'johndoe', 'time_taken': 50,
         'level': 2, 'ingredients': 'blood', 'cooking_type': 0, 'cuisine': 'Scottish',
         'description': 'bake the blood :)', 'created': now},]

    Chinese_Recipes = [
        {'recipe_id': 5, 'recipe_name': 'Veggie Chow Mein Noodles', 'username': 'johndoe', 'time_taken': 30,
         'level': 0, 'ingredients': 'Vegetables, Egg Noodles, Soy Sauce', 'cooking_type': 1, 'cuisine': 'Chinese',
         'description': 'Boil noodles, add veggies, bon apetit :)', 'created': now},]

    Romanian_Recipes = [
        {'recipe_id': 6, 'recipe_name': 'Polenta', 'username': 'johndoe', 'time_taken': 50,
         'level': 0, 'ingredients': 'cornflower', 'cooking_type': 2, 'cuisine': 'Romanian',
         'description': 'Cook cornflower :)', 'created': now},]

    Lebanese_Recipes = [
        {'recipe_id': 7, 'recipe_name': 'Stuffed Vine Leaves', 'username': 'johndoe', 'time_taken': 120,
         'level': 2, 'ingredients': 'Vine leaves, salt, rice, veggies, tomato salsa', 'cooking_type': 0, 'cuisine': 'Lebanese',
         'description': 'Stuff the vine leaves :)', 'created': now},]

    Mauritian_Recipes = [
        {'recipe_id': 8, 'recipe_name': 'Boulettes', 'username': 'johndoe', 'time_taken': 60,
         'level': 1, 'ingredients': 'fish, onion, coriander', 'cooking_type': 0, 'cuisine': 'Mauritian',
         'description': 'Mix all and steam the fish :)', 'created': now},]

    Other_Recipes = []

    cuisines = ['Italian','Egyptian','Indian','Scottish','Chinese','Romanian','Lebanese','Mauritian','Others']

    for cuisine in cuisines:
        c=add_cuisine(cuisine)
        for p in cat_data['pages']:
            add_recipe(c,p['title'],p['url'],p['views'])

    for c in Cuisine.objects.all():
        for p in Recipe.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_recipe(id,recipe_name,username, time_taken,level,ingredients,cooking_type,cuisine,description):
    p = Recipe.objects.get_or_create(recipe_id=id,recipe_name=recipe_name,username= username,time_taken= time_taken,
    level= level, ingredients= ingredients, cooking_type= cooking_type, cuisine= cuisine, description= description)[0]
    p.save()
    return p

def add_cuisine(name):
    c=Cuisine.objects.get_or_create(name=name)[0]
    c.save()
    return c

if __name__=='__main__':
    print('Starting Rango population script...')
    populate()
