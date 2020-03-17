from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from breakingbread.forms import *
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from breakingbread.models import *;
import json;
import math;

# Create your views here.
def index(request):
    logged_in=False
    username=""
  
    if request.user.is_authenticated:
        logged_in=True
        username=request.user.username
    else:
        logged_in=False

    
    recipes_images = Image.objects.all()
    vegan_recipes = []
    for i in recipes_images:
        if i.recipe_id.cooking_type == 2:
            vegan_recipes.append(i)
    vegetarian_recipes = []
    for i in recipes_images:
        if i.recipe_id.cooking_type == 1:
            vegetarian_recipes.append(i)
    
    best_vegan = sorted(vegan_recipes, key= lambda t: t.recipe_id.average_rating, reverse = True)[0:1]
    best_vegetarian = sorted(vegetarian_recipes, key= lambda t: t.recipe_id.average_rating, reverse = True)[0:1]
    best_sorted = sorted(recipes_images, key= lambda t: t.recipe_id.average_rating, reverse = True)

    best_set_id = set()
    best_set = []
    for i in best_sorted:
        if i.recipe_id not in best_set_id:
           best_set_id.add(i.recipe_id)
           best_set.append(i)
  
    best_recipes_images = best_set[0:6]
  
    context_dict={"logged_in":logged_in, "username":username, "best_recipes": best_recipes_images, "best_vegan": best_vegan, "best_vegetarian":best_vegetarian}
    response = render(request, 'breakingbread/index.html', context=context_dict)
    return response

def register(request):
    registered=False
    if request.method=="POST":
        user_form=SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered=True
        else:
            context_dict = {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered,
                            'user_form_errors':user_form.errors,
                            'profile_form_errors':profile_form.errors}
            print('errors_use', user_form.errors)
            return render(request,'breakingbread/register.html',context=context_dict)
    else:
        user_form=SignUpForm()
        profile_form=UserProfileForm()
    context_dict = {'user_form':user_form,'profile_form':profile_form,'registered':registered}
    return render(request,'breakingbread/register.html',context=context_dict)

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('breakingbread:index'))
            else:
                return render(request, 'breakingbread/login.html',context={"error":"Your account has been disabled"})
                #return HttpResponse("Your account is disabled.")
        else:
            #print(f"Invalid login details: {username}, {password}")
            #return HttpResponse("Incorrect username or password")
            return render(request, 'breakingbread/login.html',context={"error":"Incorrect username or password!"})
    else:
        return render(request, 'breakingbread/login.html')
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('breakingbread:index'))

def recipe(request):
    recipe_ = Recipe.objects.filter(recipe_id = 1)
    # decimal = [1]
    # #print(type(recipe))
    # if recipe_[0].average_rating == math.floor(recipe_[0].average_rating):
    #     print(recipe_[0].average_rating, math.floor(recipe_[0].average_rating))
    #     decimal = []
    # recipe = {"id": recipe_[0].recipe_id,
    #                    "name": recipe_[0].recipe_name,
    #                    "username": recipe_[0].username,
    #                    "rating_ceil": list(range(5 - math.ceil(recipe_[0].average_rating))),
    #                    # to get the number of coloured star in rating
    #                    "rating_floor": list(range(math.floor(recipe_[0].average_rating))),
    #                    # to get the number of blank stars in rating
    #                    "rating_decimal": decimal,
    #                     "time_taken": recipe_[0].time_taken,
    #                     "level": recipe_[0].level,
    #                     "ingredients": recipe_[0].ingredients,
    #                     "cooking_type": recipe_[0].cooking_type,
    #                     "cuisine": recipe_[0].cuisine,
    #                     "description": recipe_[0].description,
    #                     "created": recipe_[0].created,
    #                     "image": []
    #           }
    # print(decimal)
    # # retrieving the first image of each recipe
    # images = Image.objects.filter(recipe_id=recipe_[0].recipe_id)
    # for image in images:
    #     recipe["image"].append(image.picture)
    return render(request, 'breakingbread/receipe-post.html', {'recipe':recipe_})

#@login_required
def review(request):
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Save the new review to the database.
            print(form.message)
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect(reverse('breakingbread:recipe'))
        else:
        # The supplied form contained errors
        # just print them to the terminal.
            print(form.errors)
        # Will handle the bad form, new form, or no form supplied cases.
        # Render the form with error messages (if any).
    return render(request, '/breakingbread/receipe-post.html', {'form': form})


    
def cuisine_list(request):
    cuisine_list=[];
    #retrieving the cuisine list
    cuisines = Cuisine.objects.all();
    for cuisine in cuisines:
        cuisine_list.append(cuisine.cuisine_type)
    return JsonResponse({1:cuisine_list})
#retrieving search results
def search(request):
    cuisine_list = []
    #retrieving the cuisine list
    cuisines = Cuisine.objects.all();
    for cuisine in cuisines:
        cuisine_list.append(cuisine.cuisine_type)
    context_dict={}
       #retrieving the recipes
    recipes = Recipe.objects.all();
    recipes_list=[]
    for recipe in recipes:
        #checking if the rating has a decimal part
        decimal = [1]
        if recipe.average_rating == math.floor(recipe.average_rating):
            print(recipe.average_rating,math.floor(recipe.average_rating))
            decimal=[]
        recipe_list={"id":recipe.recipe_id,
                     "name":recipe.recipe_name,
                     "username":recipe.username,
                     "rating_ceil":list(range(5-math.ceil(recipe.average_rating))),#to get the number of coloured star in rating
                     "rating_floor":list(range(math.floor(recipe.average_rating))),#to get the number of blank stars in rating
                     "rating_decimal":decimal}
        print(decimal)
        #retrieving the first image of each recipe
        images = Image.objects.filter(recipe_id=recipe.recipe_id)
        for image in images:
            recipe_list["image"]=image.picture
            break
        recipes_list.append(recipe_list)
    #function to increment the value in last index of rating_floor for sorting
    def true_floor(x):
        if x["rating_floor"]!=[]:
            floor_range = x["rating_floor"]
            floor = floor_range[-1]+1
        
            return floor + 0.5
        else:
            return 0;
    #sort the list based on rating
    recipes_list.sort(key=lambda x:true_floor(x),reverse=True)   
    context_dict["recipes"]=recipes_list
    context_dict["cuisines"]= cuisine_list
    response = render(request, 'breakingbread/search-results.html',context=context_dict)
    return response
    
    


