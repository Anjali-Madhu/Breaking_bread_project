import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'breaking_bread_project.settings')
from django.utils.timezone import now
import django
django.setup()
from breakingbread.models import *
import random

user = UserProfile.objects.all()


def populate():
    Cuisine.objects.all().delete()
    Recipe.objects.all().delete()
    
    cuisines = ['Italian',
                'Indian',
                'Egyptian',
                'Scottish',
                'Chinese',
                'Romanian',
                'Lebanese',
                'Mauritian']
    for cuisine in cuisines:
        c=add_cuisine(cuisine)
    c= Cuisine.objects.all()
    
    Recipes = [
        {'recipe_id': 1, 'recipe_name': 'Bruschetta', 'username': 'johndoe', 'time_taken': 20,
         'level': 0, 'ingredients': 'tomato,garlic,bread', 'cooking_type': 1, 'cuisine': c[0],
         'description': 'Mix all :)', 'created': now},
       {'recipe_id': 2, 'recipe_name': 'Tandoori Chicken', 'username': 'johndoe', 'time_taken': 50,
         'level': 1, 'ingredients': 'chicken, spices, onion', 'cooking_type': 0, 'cuisine': c[1],
         'description': 'Cook chicken :)', 'created': now},
    
        {'recipe_id': 3, 'recipe_name': 'Koshari', 'username': 'johndoe', 'time_taken': 60,
         'level': 1, 'ingredients': 'pasta, lentils, onions, garlic, vinegar, chickpeas, rice, salsa', 'cooking_type': 1, 'cuisine': c[2],
         'description': 'Mix and fry the onions :)', 'created': now},

    
        {'recipe_id': 4, 'recipe_name': 'Black Pudding', 'username': 'johndoe', 'time_taken': 50,
         'level': 2, 'ingredients': 'blood', 'cooking_type': 0, 'cuisine': c[3],
         'description': 'bake the blood :)', 'created': now},

    
        {'recipe_id': 5, 'recipe_name': 'Veggie Chow Mein Noodles', 'username': 'johndoe', 'time_taken': 30,
         'level': 0, 'ingredients': 'Vegetables, Egg Noodles, Soy Sauce', 'cooking_type': 1, 'cuisine': c[4],
         'description': 'Boil noodles, add veggies, bon apetit :)', 'created': now},

    
        {'recipe_id': 6, 'recipe_name': 'Polenta', 'username': 'johndoe', 'time_taken': 50,
         'level': 0, 'ingredients': 'cornflower', 'cooking_type': 2, 'cuisine': c[5],
         'description': 'Cook cornflower :)', 'created': now},

    
        {'recipe_id': 7, 'recipe_name': 'Stuffed Vine Leaves', 'username': 'johndoe', 'time_taken': 120,
         'level': 2, 'ingredients': 'Vine leaves, salt, rice, veggies, tomato salsa', 'cooking_type': 0, 'cuisine': c[6],
         'description': 'Stuff the vine leaves :)', 'created': now},

    
        {'recipe_id': 8, 'recipe_name': 'Boulettes', 'username': 'johndoe', 'time_taken': 60,
         'level': 1, 'ingredients': 'fish, onion, coriander', 'cooking_type': 0, 'cuisine': c[7],
         'description': 'Mix all and steam the fish :)', 'created': now},]

    Other_Recipes = []

    cuisines = ['Italian',
                'Egyptian',
                'Indian',
                'Scottish',
                'Chinese',
                'Romanian',
                'Lebanese',
                'Mauritian']

    
    user = UserProfile.objects.all()
    r = random.randint(0,2)
    for i in Recipes:
        p= add_recipe(i['recipe_name'],user[r],i['time_taken'],
                      i['level'],i['ingredients'],i['cooking_type'],
                      i['cuisine'],i['description'])


def add_recipe(recipe_name,username, time_taken,level,ingredients,cooking_type,cuisine,description):
    p = Recipe.objects.get_or_create(recipe_name=recipe_name,username=user[0],time_taken= time_taken,
    level= level, ingredients= ingredients, cooking_type= cooking_type, cuisine= cuisine, description= description)[0]
    p.save()
    return p

def add_cuisine(cuisine):
    c=Cuisine.objects.get_or_create(cuisine_type=cuisine)[0]
    c.save()
    return c

if __name__=='__main__':
    print('Starting breakingbread population script...')
    populate()
