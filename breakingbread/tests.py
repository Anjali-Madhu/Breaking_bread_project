from django.test import TestCase
from breakingbread.models import Recipe
from breakingbread.models import User
from breakingbread.models import Cuisine
from django.urls import reverse
from django.db.models import Q
from django.utils.timezone import now

class RecipeMethodTests(TestCase):

    def test_ensure_recipe_levels_between_boundaries(self):
        """
        Ensures the levels of recipes valid
        """
        # Add users to local db
        for u in Users: 
            add_users(u)
        selected_users = User.objects.filter( Q(username = "JohnDoe") | Q(username = "EmmaWatson") ) # get only the users that we want to use

        # Add cuisines to local db
        for cuisine in cuisines:
            add_cuisine(cuisine)
        all_cuisines = Cuisine.objects.all()

        # Create a Recipe
        recipe = Recipe(recipe_id = 1, username=selected_users[0], recipe_name='test', time_taken = 12, cuisine=all_cuisines[0], level = -1, ingredients="lala", cooking_type = 0, description="")
        recipe.save()
        self.assertEqual((recipe.level >= 0 and recipe.level <= 2  ), True) # Validate the tests if 0 <= level <= 2

    def test_ensure_recipe_cooking_type_between_boundaries(self):
        """
        Ensures the cooking type of recipes valid
        """
        # Add users to local sdb
        for u in Users:
            add_users(u)
        selected_users = User.objects.filter( Q(username = "JohnDoe") | Q(username = "EmmaWatson") )

        # Add cuisines to local db
        for cuisine in cuisines:
            add_cuisine(cuisine)
        all_cuisines = Cuisine.objects.all()

        # Create a Recipe
        recipe = Recipe(recipe_id = 1, username=selected_users[0], recipe_name='test', time_taken = 12, cuisine=all_cuisines[0], level = 1, ingredients="lala", cooking_type = 5, description="")
        recipe.save()
        self.assertEqual((recipe.cooking_type >= 0 and recipe.cooking_type <= 2  ), True) # Validate the tests if 0 <= cooking_type <= 2

class SearchViewTests(TestCase):
    def test_search_view_with_no_recipes(self):
        """
        If no recipes exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('breakingbread:search'))  # Get response from search template
        self.assertEqual(response.status_code, 200) # Check the response was successful
        self.assertContains(response, 'No recipes found for your search') # Check the response contains the sentence mentioned
        self.assertQuerysetEqual(response.context['recipes'], []) # Check the list of recipes is empty

    def test_search_view_with_recipes(self):
        """
        Checks whether recipes are displayed correctly when present.
        """
        # Add users to db
        for u in Users:
            add_users(u)

        selected_users = User.objects.filter( Q(username = "JohnDoe") | Q(username = "EmmaWatson") )

        for cuisine in cuisines:
            add_cuisine(cuisine)
        all_cuisines = Cuisine.objects.all()

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
        ]

        # Add recipes to db
        for i in Recipes:
            add_recipe(i['recipe_id'], i['recipe_name'], i['username'], i['time_taken'], i['level'],i['ingredients'],i['cooking_type'], i['cuisine'],i['description'])
    
        response = self.client.get(reverse('breakingbread:search')) # get response from search page
        self.assertEqual(response.status_code, 200) # Check the response was successful
        self.assertContains(response, "Bruschetta") # Check the response contains the recipes
        self.assertContains(response, "Tandoori Chicken")
        self.assertContains(response, "Koshari")
        num_recipes = len(response.context['recipes']) # Check the list of recipes
        self.assertEquals(num_recipes, 3)


# HELPER FUNCTIONS
def add_recipe(recipe_id, recipe_name,username, time_taken,level,ingredients,cooking_type,cuisine,description):
    recipe = Recipe.objects.get_or_create(recipe_id = recipe_id, username = username, cuisine = cuisine, time_taken = time_taken, level = level)[0] 
    recipe.recipe_name=recipe_name
    recipe.ingredients= ingredients
    recipe.cooking_type= cooking_type
    recipe.description= description
    recipe.save()
    return recipe


Users = [ {'username': 'JohnDoe', 'password':'JohnDoe123', 'first_name': 'John', 'last_name': 'Doe'},
          {'username': 'EmmaWatson', 'password':'EmmaWatson123', 'first_name': 'Emma', 'last_name': 'Watson'},
        ]

def add_users(u):
    user = User.objects.get_or_create(username = u['username'], password = u['password'])[0]
    user.first_name = u['first_name']
    user.last_name = u['last_name']
    user.save()
    return user

cuisines = ['Italian',
                'Indian',
                'Egyptian',
                'Scottish',
                'Chinese',
                'Romanian',
                'Lebanese',
                'Mauritian',
                'American']
   
def add_cuisine(cuisine):
    c = Cuisine.objects.get_or_create(cuisine_type=cuisine)[0]
    c.save()
    return c


