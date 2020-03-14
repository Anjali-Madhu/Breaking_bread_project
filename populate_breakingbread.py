import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'breaking_bread_project.settings')
from django.utils.timezone import now
import django
django.setup()
from breakingbread.models import *
import random
from django.core.files import File

#https://www.bbcgoodfood.com/recipes/ source of recipe descriptions

def populate():
    Cuisine.objects.all().delete()
    Recipe.objects.all().delete()
    #User.objects.all().delete()
    UserProfile.objects.all().delete()
    Review.objects.all().delete()

    
    Users = [ {'username': 'John Doe', 'password':'1234', 'first_name': 'John', 'last_name': 'Doe'},
             {'username': 'Emma Watson', 'password':'1234', 'first_name': 'Emma', 'last_name': 'Watson'},
             ]
    for u in Users:
        add_users(u)
    all_users = User.objects.all()

    UsersProfile = [
        { 'user': all_users[0],
         'usertype': 0,
         'address': '61 Kelvinhaugh Street',
         'picture': 'populate_profile_images/profile1.jpg'
         },
         { 'user': all_users[1],
         'usertype': 1,
         'address': '11 Buchanan Street',
         'picture': 'populate_profile_images/profile2.jpg'
         }
        ]

    for u in UsersProfile:
        add_usersProfile(u)
    all_usersProfile = UserProfile.objects.all()
    
    cuisines = ['Italian',
                'Indian',
                'Egyptian',
                'Scottish',
                'Chinese',
                'Romanian',
                'Lebanese',
                'Mauritian']
    
    for cuisine in cuisines:
        add_cuisine(cuisine)

    all_cuisines = Cuisine.objects.all()
    
    Recipes = [
        {'recipe_id': 1, 'recipe_name': 'Bruschetta', 'username': all_usersProfile[0], 'time_taken': 20,
         'level': 0, 'ingredients': ['Half small red onion, finely chopped', '8 medium tomatoes (about 500g), coarsely chopped and drained', '2-3 garlic cloves, crushed',' 6-8 leaves of fresh basil finely chopped','30ml balsamic vinegar', '60-80ml extra virgin olive oil', '1 loaf crusty bread'], 'cooking_type': 1, 'cuisine': all_cuisines[0],
         'description': ['In a large bowl, mix the onions, tomatoes, garlic and basil, taking care not to mash or break up the tomatoes too much.',' Add the balsamic vinegar and extra virgin olive oil.',' Add salt and pepper to taste. Mix again. Cover and chill for at least an hour. This will allow the flavours to soak and blend together',
                        'Slice the baguette loaf diagonally into 12 thick slices and lightly toast them until they are light brown on both sides. Serve the mixture on the warm slices of bread. If you prefer the mixture at room temperature, remove from the fridge half an hour before serving'], 'created': now},

       {'recipe_id': 2, 'recipe_name': 'Tandoori Chicken', 'username': all_usersProfile[1], 'time_taken': 50,
         'level': 1, 'ingredients':[ 'Juice 2 lemons', '4 tsp paprika', '2 red onions, finely chopped', '16 skinless chicken thighs', 'vegetable oil, for brushing', '300ml Greek yogurt', 'large piece ginger, grated', '4 garlic cloves, crushed' , 'Three quarter tsp garam masala', 'Three quarter tsp ground cumin', 'half tsp chilli powder', 'Quarter tsp turmeric'], 'cooking_type': 0, 'cuisine': all_cuisines[1],
         'description': ['Mix the lemon juice with the paprika and red onions in a large shallow dish. Slash each chicken thigh three times, then turn them in the juice and set aside for 10 mins.','Mix all of the marinade ingredients together and pour over the chicken. Give everything a good mix, then cover and chill for at least 1 hr. This can be done up to a day in advance.','Heat the grill. Lift the chicken pieces onto a rack over a baking tray. Brush over a little oil and grill for 8 mins on each side or until lightly charred and completely cooked through.'], 'created': now},
    
        {'recipe_id': 3, 'recipe_name': 'Koshari', 'username': all_usersProfile[0], 'time_taken': 60,
         'level': 1, 'ingredients': 'pasta, lentils, onions, garlic, vinegar, chickpeas, rice, salsa', 'cooking_type': 1, 'cuisine': all_cuisines[2],
         'description': 'Mix and fry the onions :)', 'created': now},

    
        {'recipe_id': 4, 'recipe_name': 'Black Pudding', 'username': all_usersProfile[1], 'time_taken': 50,
         'level': 2, 'ingredients': 'blood', 'cooking_type': 0, 'cuisine': all_cuisines[3],
         'description': 'bake the blood :)', 'created': now},

    
        {'recipe_id': 5, 'recipe_name': 'Veggie Chow Mein Noodles', 'username': all_usersProfile[0], 'time_taken': 30,
         'level': 0, 'ingredients': 'Vegetables, Egg Noodles, Soy Sauce', 'cooking_type': 1, 'cuisine': all_cuisines[4],
         'description': 'Boil noodles, add veggies, bon apetit :)', 'created': now},

    
        {'recipe_id': 6, 'recipe_name': 'Polenta', 'username': all_usersProfile[0], 'time_taken': 50,
         'level': 0, 'ingredients': 'cornflower', 'cooking_type': 2, 'cuisine': all_cuisines[5],
         'description': 'Cook cornflower :)', 'created': now},

    
        {'recipe_id': 7, 'recipe_name': 'Stuffed Vine Leaves', 'username': all_usersProfile[0], 'time_taken': 120,
         'level': 2, 'ingredients': 'Vine leaves, salt, rice, veggies, tomato salsa', 'cooking_type': 0, 'cuisine': all_cuisines[6],
         'description': 'Stuff the vine leaves :)', 'created': now},

    
        {'recipe_id': 8, 'recipe_name': 'Boulettes', 'username': all_usersProfile[1], 'time_taken': 60,
         'level': 1, 'ingredients': 'fish, onion, coriander', 'cooking_type': 0, 'cuisine': all_cuisines[7],
         'description': 'Mix all and steam the fish :)', 'created': now},
    ]

    
    for i in Recipes:
        add_recipe(i['recipe_id'], i['recipe_name'], i['username'], i['time_taken'],
                      i['level'],i['ingredients'],i['cooking_type'],
                      i['cuisine'],i['description'])

    all_recipes = Recipe.objects.all()

    Images = [
         {'image_id': 1,
          'picture':  'populate_recipe_images/bruschetta.jpg',
          'recipe_id': all_recipes[0]
         },
         {'image_id': 2,
          'picture':  'populate_recipe_images/tandoori_chicken.jpg',
          'recipe_id': all_recipes[1]
         },
         {'image_id': 3,
          'picture':  'populate_recipe_images/koshari.jpg',
          'recipe_id': all_recipes[2]
         },
         {'image_id': 4,
          'picture':  'populate_recipe_images/black_pudding.jpg',
          'recipe_id': all_recipes[3]
         },
         {'image_id': 5,
          'picture':  'populate_recipe_images/chow_mein.jpg',
          'recipe_id': all_recipes[4]
         },
         {'image_id': 6,
          'picture':  'populate_recipe_images/polenta.jpg',
          'recipe_id': all_recipes[5]
         },
         {'image_id': 7,
          'picture':  'populate_recipe_images/stuffed_vine_leaves.jpg',
          'recipe_id': all_recipes[6]
         },
         {'image_id': 8,
          'picture':  'populate_recipe_images/boulettes.jpg',
          'recipe_id': all_recipes[7]
         },
         ]

    for img in Images:
        add_image(img['image_id'], img['picture'], img['recipe_id'])

    Reviews = [{'review_id': 1, 'recipe_id': all_recipes[1], 'username': all_usersProfile[1], 'rating': 5, 'description': 'very tasty', 'date': '12/03/2020'},]
    for rev in Reviews:
        add_review(rev)

def add_review(rev):
    review = Review.objects.get_or_create(review_id = rev['review_id'], recipe_id = rev['recipe_id'], username = rev['username'])[0]
    review.rating = rev['rating']
    review.description = rev['description']
    review.date = rev['date']
    review.save()
    return review


def add_users(u):
    user = User.objects.get_or_create(username = u['username'], password = u['password'])[0]
    user.first_name = u['first_name']
    user.last_name = u['last_name']
    user.save()
    return user

def add_usersProfile(u):
    user = UserProfile.objects.get_or_create(user = u['user'])[0]
    user.usertype = u['usertype']
    user.address = u['address']
    user.picture = u['picture']
    user.save()
    return user
 


def add_recipe(recipe_id, recipe_name,username, time_taken,level,ingredients,cooking_type,cuisine,description):
    recipe = Recipe.objects.get_or_create(recipe_id = recipe_id, username = username, cuisine = cuisine, time_taken = time_taken, level = level)[0] 
    recipe.recipe_name=recipe_name
    recipe.ingredients= ingredients
    recipe.cooking_type= cooking_type
    recipe.description= description
    recipe.save()
    return recipe

def add_cuisine(cuisine):
    c = Cuisine.objects.get_or_create(cuisine_type=cuisine)[0]
    c.save()
    return c

def add_image(image_id, picture, recipe_id):
    img = Image.objects.get_or_create(image_id = image_id, recipe_id = recipe_id)[0]
    img.picture = picture
    img.save()
    return img

if __name__=='__main__':
    print('Starting breakingbread population script...')
    populate()
