import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'breaking_bread_project.settings')
from django.utils.timezone import now
import django
django.setup()
from breakingbread.models import *
import random
from django.core.files import File
from django.db.models import Q

#https://www.bbcgoodfood.com/recipes/ and https://www.epicurious.com/recipes/food/views/black-pudding-51145600 are the sources of recipe descriptions
#http://www.foodnetwork.co.uk/recipes/voulas-offshore-cafe-stuffed-grape-leaves-0.html for the stuffed vine leaves recipe
# Smoothie: https://aseasyasapplepie.com/tropical-raspberry-swirl-smoothie/
# Boulettes: https://www.allrecipes.com/recipe/197908/crawfish-boulettes/
def populate():
    # Delete all the data from database except the admin
    Cuisine.objects.all().delete()
    Recipe.objects.all().delete()
    User.objects.filter(~Q(username="admin")).delete()
    UserProfile.objects.all().delete()
    Review.objects.all().delete()
    Report.objects.all().delete()

    # Create users
    Users = [ {'username': 'JohnDoe', 'password':'JohnDoe123', 'first_name': 'John', 'last_name': 'Doe'},
             {'username': 'EmmaWatson', 'password':'EmmaWatson123', 'first_name': 'Emma', 'last_name': 'Watson'},
             {'username': 'janedoe', 'password':'j@nedoe666', 'first_name': 'Jane', 'last_name': 'Doe'},
             ]

    # Add users to db
    for u in Users:
        add_users(u)
    all_users = User.objects.all()
    selected_users = User.objects.filter( Q(username = "JohnDoe") | Q(username = "EmmaWatson")|Q(username="janedoe" ) )# get only the users that we want to use

    # Create users profile
    UsersProfile = [
        { 'user': selected_users[0],
         'usertype': 0,
         'address': '61 Kelvinhaugh Street',
         'picture': 'populate_profile_images/profile2.jpg'
         },
         { 'user': selected_users[1],
         'usertype': 1,
         'address': '11 Buchanan Street',
         'picture': 'populate_profile_images/profile1.jpg'
         }
        ]

    # Add users profile to db
    for u in UsersProfile:
        add_usersProfile(u)
    all_usersProfile = UserProfile.objects.all() # get all user profiles
    
    cuisines = ['Italian',
                'Indian',
                'Egyptian',
                'Scottish',
                'Chinese',
                'Romanian',
                'Lebanese',
                'Mauritian',
                'American']

    # Add cuisines to db
    for cuisine in cuisines:
        add_cuisine(cuisine)
    all_cuisines = Cuisine.objects.all() # get all cuisines
    
    # Define recipes
    Recipes = [
        {'recipe_id': 1, 'recipe_name': 'Bruschetta', 'username': selected_users[0], 'time_taken': 20,
         'level': 0, 'ingredients': 'Half small red onion, finely chopped?8 medium tomatoes (about 500g), coarsely chopped and drained?2-3 garlic cloves, crushed? 6-8 leaves of fresh basil finely chopped?30ml balsamic vinegar?60-80ml extra virgin olive oil?1 loaf crusty bread', 'cooking_type': 1, 'cuisine': all_cuisines[0],
         'description': 'In a large bowl, mix the onions, tomatoes, garlic and basil, taking care not to mash or break up the tomatoes too much.? Add the balsamic vinegar and extra virgin olive oil.? Add salt and pepper to taste. Mix again. Cover and chill for at least an hour. This will allow the flavours to soak and blend together?Slice the baguette loaf diagonally into 12 thick slices and lightly toast them until they are light brown on both sides. Serve the mixture on the warm slices of bread. If you prefer the mixture at room temperature, remove from the fridge half an hour before serving', 'created': now},

       {'recipe_id': 2, 'recipe_name': 'Tandoori Chicken', 'username': selected_users[1], 'time_taken': 50,
         'level': 1, 'ingredients':'Juice 2 lemons?4 tsp paprika?2 red onions, finely chopped?16 skinless chicken thighs?vegetable oil, for brushing?300ml Greek yogurt?large piece ginger, grated?4 garlic cloves, crushed?Three quarter tsp garam masala?Three quarter tsp ground cumin?half tsp chilli powder?Quarter tsp turmeric', 'cooking_type': 0, 'cuisine': all_cuisines[1],
         'description': 'Mix the lemon juice with the paprika and red onions in a large shallow dish.? Slash each chicken thigh three times, then turn them in the juice and set aside for 10 mins.?Mix all of the marinade ingredients together and pour over the chicken.?Give everything a good mix, then cover and chill for at least 1 hr. This can be done up to a day in advance.?Heat the grill. Lift the chicken pieces onto a rack over a baking tray.?Brush over a little oil and grill for 8 mins on each side or until lightly charred and completely cooked through.', 'created': now},
    
        {'recipe_id': 3, 'recipe_name': 'Koshari', 'username': selected_users[0], 'time_taken': 60,
         'level': 1, 'ingredients': '120g dried brown lentils?120g white long grain rice?2 small celeriac?2 garlic bulb, split across the middle?150ml rapeseed oil?Rapeseed oil or extra virgin olive oil?4 onions?120g macaroni?2 tbsp pine nuts?1 tsp cumin seeds?Coriander seeds?400ml vegetable stock?1 lemon, zested and juiced', 'cooking_type': 1, 'cuisine': all_cuisines[2],
         'description': 'Heat oven to 180C/160C fan/gas 4. Rinse the lentils and rice together under cold water until the water runs clear. Soak them in water for 30 mins, then drain. Meanwhile, toss the celeriac and garlic halves in 4 tbsp of the rapeseed oil and season. Cover with foil and roast for 20 mins, tossing occasionally. Remove the foil '
                         'and return to the oven for 10 mins until soft and caramelised.?Heat 4 tbsp of the oil over a medium heat, season and fry the onions for about 12 mins until starting to caramelise. In the meantime, cook the macaroni until al dente, then drain. Tip into the onions along with the pine nuts, fry until the nuts and pasta are starting to brown, then remove from the heat.?Heat the remaining 2 tbsp oil in a heavy-bottomed frying pan and add the ground cinnamon, cumin and coriander seeds. Stir until they sizzle, then add the lentils and rice. Stir-fry for 1 min, then add the stock and cranberries.'
                        ' Cook for about 25 mins, stirring occasionally, until the stock is absorbed and the cranberries have swelled up.?Tip the lentil mixture into the onion mixture along with the celeriac, and heat over a medium heat to warm it all through. Squeeze the roasted garlic cloves out of their skins and mash with the lemon zest and juice, then stir into the rice.?In a separate container, stir the harissa into the yogurt. To serve, divide the koshari between bowls and top with the spiced yogurt and coriander.', 'created': now},

    
        {'recipe_id': 4, 'recipe_name': 'Black Pudding', 'username': selected_users[1], 'time_taken': 50,
         'level': 2, 'ingredients': '4 cups fresh pig"s blood?2 1/2 teaspoons salt?1 1/2 cups steel-cut (pinhead) oatmeal?2 cups finely diced pork fat (or beef suet), finely chopped?'
            '1 large yellow onion, finely chopped?1 cup milk?1 1/2 teaspoons freshly ground black pepper?1 teaspoon ground allspice', 'cooking_type': 0, 'cuisine': all_cuisines[3],
         'description': 'Preheat the oven to 325°F and grease 2 glass loaf pans. (If you don"t have glass loaf pans, line metal loaf pans with parchment to keep the blood sausage from reacting with the metal and creating an off-flavor.) Stir 1 teaspoon of salt into the blood.?'
                        'Bring 2 1/2 cups water to a boil and stir in the oats. Simmer, stirring occasionally, for 15 minutes, until just tender, not mushy.?Pour the blood through a fine sieve into a large bowl to remove any lumps. Stir in the fat, onion, milk, pepper, allspice and remaining 1 1/2 teaspoons salt. Add the oatmeal and mix to combine. Divide the mixture between the loaf pans, cover with foil, and bake for 1 hour, until firm. Cool completely. '
                        'Seal in plastic wrap and wither freeze for extended use or store in the refrigerator for up to a week.?To serve, cut a slice about 1/2-inch thick off the loaf. Fry in butter or oil until the edges are slightly crisped and browned.','created': now},

        {'recipe_id': 5, 'recipe_name': 'Veggie Chow Mein Noodles', 'username': selected_users[0], 'time_taken': 30,
         'level': 0, 'ingredients': 'Vegetables? Egg Noodles? Soy Sauce', 'cooking_type': 1, 'cuisine': all_cuisines[4],
         'description': 'Cook 225g egg noodles in a large pan of boiling water for 3-5 mins, then drain and put them in '
                        'cold water. Drain thoroughly, toss them with 1 tbsp sesame oil and set aside.?Add the noodles, 2 tsp light soy sauce, 2 tsp dark soy sauce,1 tbsp Shaohsing rice wine or dry sherry,'
                        ' ½ tsp white pepper, ½ tsp golden caster sugar, 2 finely chopped spring onions and 1 tsp salt.?Stir-fry for about 2 mins and then transfer to a plate.', 'created': now},

    
        {'recipe_id': 6, 'recipe_name': 'Polenta', 'username': selected_users[0], 'time_taken': 50,
         'level': 0, 'ingredients': '175g of quick-cook Polenta?5 tbsp vegan mascarpone', 'cooking_type': 2, 'cuisine': all_cuisines[5],
         'description': 'Cook the polenta according to pack instructions. When the polenta is softened and smooth, stir through the mascarpone ', 'created': now},

    
        {'recipe_id': 7, 'recipe_name': 'Stuffed Vine Leaves', 'username': selected_users[0], 'time_taken': 120,
         'level': 2, 'ingredients': '2 tbsp olive oil 450g minced beef 1/2 onion, finely diced 100g rice 2 cloves garlic, finely chopped,'
                                     '20g freshly chopped parsley leaves?10g freshly chopped dill,1 tsp salt?1 tsp freshly ground black pepper?5g dried oregano.'
                                     '1 jar grape leaves?Water?30g butter', 'cooking_type': 0, 'cuisine': all_cuisines[6],
         'description': 'In a large sauté pan over medium-high heat, add the oil. Once heated, add: minced beef, onions, rice and garlic and sauté until the mince has browned.? '
                        'Remove from heat; stir in parsley, dill, salt, pepper and oregano. Set aside to cool a bit.?Place grape leaves in a bowl and pour water over leaves.?'
                        'Soak for 15 minutes and drain. Transfer leaves, dull-side down, to kitchen paper to dry.?Preheat oven to 190C/Gas Mark 5.?'
                         'Stuff grape leaves using 1 heaping tablespoon mixture in centre of the dull-side of the leaf and fold outer parts toward the centre; '
                         'and roll up like you would a burrito. Do not roll too tightly.? Arrange rolls in side by side layers in a deep baking pan. Once complete, fill the pan with water to the top of the grape leaves and place the butter on top.? '
                         'Cover with foil and bake 1 hour or until the water has been absorbed by the grape leaves.', 'created': now},

    
        {'recipe_id': 8, 'recipe_name': 'Boulettes', 'username': selected_users[1], 'time_taken': 60,
         'level': 1, 'ingredients': '1 (16 ounce) package cooked and peeled whole crawfish tails?1/2 cup chopped onion?1/4 cup chopped green bell pepper?1/4 cup chopped celery?'
                                     '1 1/2 teaspoons minced garlic?5 slices stale white bread, torn into pieces?1 egg?1 teaspoon salt?1/2 teaspoon black pepper?2 teaspoons Cajun seasoning?2 tablespoons chopped fresh parsley?'
                                     '3 tablespoons thinly sliced green onions? 2 quarts vegetable oil for frying?1 1/2 cups dry bread crumbs?1 tablespoon Cajun seasoning', 'cooking_type': 0, 'cuisine': all_cuisines[7],
         'description': 'Place the crawfish tails, chopped onion, bell pepper, celery, garlic, stale bread, and egg into the bowl of a food processor. Add the salt, black pepper, and 2 teaspoons of Cajun seasoning. Cover and pulse until the crayfish mixture is finely chopped. '
                         'Scrape into a bowl and fold in the parsley and green onions. Cover and refrigerate 1 hour.?Heat oil in a deep-fryer or large saucepan to 350 degrees F (175 degrees C). '
                        'Whisk the bread crumbs and 1 tablespoon of Cajun seasoning together in a bowl; set aside. ?Form the crawfish mixture into 1 tablespoon-size balls and roll in the bread crumbs. Cook in batches in the hot oil until the balls turn golden brown and '
                         'begin to float, about 4 minutes. Drain on a paper towel-lined plate and serve hot.', 'created': now},

        {'recipe_id': 9, 'recipe_name': 'Cheeseburger', 'username': selected_users[0], 'time_taken': 60,
         'level': 1, 'ingredients': '1kg minced beef?'
                                     '300g breadcrumbs?'
                                     '140g extra-mature or mature cheddar, grated?4 tbsp Worcestershire sauce?'
                                     '1 small bunch parsley, finely chopped?2 eggs, beaten?split burger buns?sliced tomatoes?red onion slices?tomato sauce, coleslaw, wedges or fries',
         'cooking_type': 0, 'cuisine': all_cuisines[8],
         'description': 'Crumble the mince in a large bowl, then tip in the breadcrumbs, cheese, Worcestershire sauce, parsley and eggs with 1 tsp ground pepper and 1-2 tsp salt. Mix with your hands to combine everything thoroughly.?'
             'Shape the mix into 12 burgers. Chill until ready to cook for up to 24 hrs. Or freeze for up to 3 months. Just stack between squares of baking parchment to '
             'stop the burgers sticking together, then wrap well. Defrost overnight in the fridge before cooking.?To cook the burgers, heat grill to high. Grill burgers for 6-8 mins on each side until cooked through. Meanwhile, warm as many buns as you need in a foil-covered tray below the grilling burgers.'
            'Let everyone assemble their own, served with their favourite accompaniments.','created': now},

        {'recipe_id': 10, 'recipe_name': 'Summer Smoothie', 'username': selected_users[0], 'time_taken': 30,
         'level': 0, 'ingredients': '1 sliced banana fresh or frozen?150 grams (1 cup) mango chunks fresh or frozen?80 grams (1/2 cup) pineapple chunks fresh or frozen?'
'120 ml (1/2 cup) coconut water?120 grams (1 cup) frozen raspberries?1 teaspoon honey or agave more to taste?60 ml (1/4 cup) coconut water?Garnish (optional) : pineapple wedges',
         'cooking_type': 0, 'cuisine': all_cuisines[8], 'description':
             'In a blender, add the banana, mango, pineapple and coconut water. Blend until smooth and creamy, adding more coconut water if needed. Put it in a jar and refrigerate.?'
             'In the same blender (no need to wash it), puree the frozen raspberries, honey and coconut water until smooth. Add more coconut water if needed?'
             'Divide the raspberry smoothie between two glasses. Now pour the tropical smoothie on top and swirl gently with a long spoon.'
             'Garnish with pineapple wedges and serve.', 'created': now}
        ]

    # Add recipes to the db
    for i in Recipes:
        add_recipe(i['recipe_id'], i['recipe_name'], i['username'], i['time_taken'],
                      i['level'],i['ingredients'],i['cooking_type'],
                      i['cuisine'],i['description'])

    all_recipes = Recipe.objects.all() # get all recipes

    # Define images
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
        {'image_id': 9,
         'picture': 'populate_recipe_images/cheeseburger.jpg',
         'recipe_id': all_recipes[8]
         },
        {'image_id': 10,
         'picture': 'populate_recipe_images/berry_smoothie.jpg',
         'recipe_id': all_recipes[9]
         },
         ]

    # Add images to db
    for img in Images:
        add_image(img['image_id'], img['picture'], img['recipe_id'])

    # Define reviews
    Reviews = [{'review_id': 1, 'recipe_id': all_recipes[0], 'username': selected_users[1],
              'rating': 3, 'description': 'very tasty',   'date': '12/03/2020'},
               {'review_id': 2, 'recipe_id': all_recipes[1], 'username': selected_users[1],
              'rating': 5, 'description': 'a very tasty recipe ',   'date': '12/03/2020'},
              {'review_id': 3, 'recipe_id': all_recipes[2], 'username': selected_users[0],
              'rating': 5, 'description': 'very tasty',   'date': '12/03/2020'},
               {'review_id': 4, 'recipe_id': all_recipes[3], 'username': selected_users[1],
              'rating': 2, 'description': 'interesting taste',   'date': '12/03/2020'},
               {'review_id': 5, 'recipe_id': all_recipes[4], 'username': selected_users[1],
              'rating': 2, 'description': 'not very tasty',   'date': '12/03/2020'},
                {'review_id': 6, 'recipe_id': all_recipes[5], 'username': selected_users[1],
              'rating': 3, 'description': 'a very bland dish',   'date': '12/03/2020'}]
    # Add reviews to db
    for rev in Reviews:
        add_review(rev)
    all_reviews = Review.objects.all()
        
    #Define reports
    Reports = [{'report_id': 1, 'post_type': 0, 'recipe_id': all_recipes[1],
              'username': selected_users[2], 'description': 'copied from another website'},
               {'report_id': 2, 'post_type':1, 'review_id':all_reviews[4], 'username': selected_users[2],
              'description': 'the comment was very offensive'},
              ]
    for report in Reports:
        add_report(report)

# HELPER METHODS 
def add_review(rev):
    review = Review.objects.get_or_create(review_id = rev['review_id'], recipe_id = rev['recipe_id'], username = rev['username'])[0]
    review.rating = rev['rating']
    review.description = rev['description']
    review.date = rev['date']
    review.save()
    return review

def add_users(u):
    user = User.objects.get_or_create(username = u['username'])[0]
    user.set_password(u['password'])
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
def add_report(rep):
    report = Report.objects.get_or_create(report_id=rep["report_id"],post_type=rep["post_type"],username=rep["username"],description=rep["description"])[0]
    if rep["post_type"] == 0:
        report.recipe_id = rep["recipe_id"]
        report.post = rep["recipe_id"].recipe_name
        report.reported_user = rep["recipe_id"].username.username
    else:
        report.review_id = rep["review_id"]
        report.post = rep["review_id"].description
        report.reported_user = rep["review_id"].username.username
    report.save()
    return report

# Calling the script
if __name__=='__main__':
    print('Starting breakingbread population script...')
    populate()
