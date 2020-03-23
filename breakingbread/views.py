from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from breakingbread.forms import *
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from breakingbread.models import *;
from django.utils.decorators import method_decorator
import datetime
import json
import math

# Create your views here.

#method to check if any user has logged in 
def check_logged_in(request):
    logged_in=False
    username=""
    if request.user.is_authenticated:
        logged_in=True
        username=request.user.username
    else:
        logged_in=False
    return (username,logged_in)

#Homepage
def index(request):
    #checking if any user has logged in
    username,logged_in = check_logged_in(request)

    #retrieving all recipe images
    recipes_images = Image.objects.all()
    
    #filtering out the vegan recipe images and vegetarian recipe images
    vegan_recipes = []
    for i in recipes_images:
        if i.recipe_id.cooking_type == 2:
            vegan_recipes.append(i)
    vegetarian_recipes = []
    for i in recipes_images:
        if i.recipe_id.cooking_type == 1:
            vegetarian_recipes.append(i)
    
    #sorting the images from highest ratings to lowest ratings of their corresponding recipes
    best_vegan = sorted(vegan_recipes, key= lambda t: t.recipe_id.average_rating, reverse = True)[0:1]
    best_vegetarian = sorted(vegetarian_recipes, key= lambda t: t.recipe_id.average_rating, reverse = True)[0:1]
    best_sorted = sorted(recipes_images, key= lambda t: t.recipe_id.average_rating, reverse = True)

    #adding the first image of every recipe to best_set
    best_set_id = set()
    best_set = []
    for i in best_sorted:
        if i.recipe_id not in best_set_id:
           best_set_id.add(i.recipe_id)
           best_set.append(i)
  
    #contains the first images of top 5 recipes
    best_recipes_images = best_set[0:6]
    
    context_dict={"logged_in":logged_in, "username":username, "best_recipes": best_recipes_images,
                 "best_vegan": best_vegan, "best_vegetarian":best_vegetarian, "nav_tab":"home"}
    #rendering the index template and sending context_dict to the template
    response = render(request, 'breakingbread/index.html', context=context_dict)
    return response

#view for sign up page
def register(request):
    registered=False
    
    #retrieving the inputs from the page
    if request.method=="POST":
        user_form=SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST)
       
        #checking if the inputs are valid
        if user_form.is_valid() and profile_form.is_valid():
           #if the inputs are valid, saving the details in the database
            user = user_form.save()
            profile=profile_form.save(commit=False)
            profile.user = user
            #checking if the user has uploaded a profile picture
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            #setting registered = True since registeration is successful
            registered=True
        else:
            #sending the error messages along with form if registeration is unseccessful
            context_dict = {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered,
                            'user_form_errors':user_form.errors,
                            'profile_form_errors':profile_form.errors}
            print('errors_use', user_form.errors)
            return render(request,'breakingbread/register.html',context=context_dict)
    else:
        #sending the empty form if request is not a POST
        user_form=SignUpForm()
        profile_form=UserProfileForm()
    context_dict = {'user_form':user_form,'profile_form':profile_form,'registered':registered, "nav_tab":"register"}
    return render(request,'breakingbread/register.html',context=context_dict)

#login view
def user_login(request):
    if request.method == 'POST':
        #if method is POST, retrieving the username and password
        username = request.POST.get('username')
        password = request.POST.get('password')
        #if the user did not login and try to post comments and ratings
        #redirect to login and if valid login redirect to the previous page(next)
        next = request.POST.get('next', None)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if next is not None :
                   return HttpResponseRedirect(next)
                else :
                    return redirect(reverse('breakingbread:index'))
            else:
                print('error')
                return render(request, 'breakingbread/login.html',context={"error":"Your account has been disabled"})
               
        else:
            print('invalid')
            return render(request, 'breakingbread/login.html',context={"error":"Incorrect username or password!"})
    else:
        return render(request, 'breakingbread/login.html', context ={"nav_tab":"log_in"})
    
#view for log out
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('breakingbread:index'))


#view for recipe-post
def recipe(request,recipe_id):
    
    #check if any user has logged in
    username,logged_in =check_logged_in(request)
    #retrieving the recipe details from the database     
    recipe_to_display = Recipe.objects.filter(recipe_id= recipe_id)
    
    #checking if the average rating is  a whole number or a decimal
    #used for displaying ratings in stars in the format    
    decimal = [1]
    if recipe_to_display[0].average_rating == math.floor(recipe_to_display[0].average_rating):
        decimal=[]
    #adding all the recipe attributes to the context dictionary(i.e recipe_)
    recipe_ = {"id": recipe_to_display[0].recipe_id,
                        "name": recipe_to_display[0].recipe_name,
                        "user": recipe_to_display[0].username.username,
                         "time_taken": recipe_to_display[0].time_taken,
                         "level": recipe_to_display[0].level,
                         "ingredients": [],
                         "cooking_type": recipe_to_display[0].cooking_type,
                         "cuisine": recipe_to_display[0].cuisine,
                         "description": [],
                         "created": recipe_to_display[0].created,
                        "images": [],
                        "rating_ceil":list(range(5-math.ceil(recipe_to_display[0].average_rating))),#to get the number of coloured star in rating
                     "rating_floor":list(range(math.floor(recipe_to_display[0].average_rating))),#to get the number of blank stars in rating
                     "rating_decimal":decimal,
              }
    recipe_["logged_in"]=logged_in
    recipe_["username"]=username
    
    #retrieving all the images of the recipe
    images = Image.objects.filter(recipe_id=recipe_id)
    for image in images:
        recipe_["images"].append(image.picture)
    
    #different steps in descriptions in the database are seperated by a "?", therefore splitting them into a list
    for i in recipe_to_display[0].description.split("?"):
        recipe_["description"].append(i)

    #different ingredients are seperated by "?" in the database, therefore splitting them into a list
    for i in recipe_to_display[0].ingredients.split("?"):
        recipe_["ingredients"].append(i)
        
    #retrieving all the reviews/comments of the recipe
    reviews = Review.objects.filter(recipe_id = recipe_to_display[0])
    review_list = []
    for r in reviews:
        review = {"description":r.description,
                  "created":r.created,
                  "username":r.username,
                  "rating_ceil":list(range(5-r.rating)),
                  "rating_floor":list(range(r.rating))
                }
        review_list.append(review)
        #reversing the order so that the latest review comes first
        review_list.reverse()
    recipe_["reviews"] = review_list

    return render(request, 'breakingbread/receipe-post.html', context = recipe_)

#method for adding a new comment/review to database
@login_required
def review(request, recipe_id):
    
    #retrieving the recipe object for which the review has been posted
    recipe_page = Recipe.objects.filter(recipe_id= recipe_id)
    #retrieving the inputs and inserting the details in the database
    message = request.GET.get('message', None)
    rating = request.GET.get('rating', None)
    review = Review(recipe_id=recipe_page[0], username=request.user, description=message, rating=rating)
    review.save()
    data = {
        "success" : True,
    }
    #sending response to javascript
    return JsonResponse(data)

#method to retrieve all cuisine objects and send it to base html    
def cuisine_list(request):
    
    
    cuisine_list=[];
    #retrieving the cuisine list
    cuisines = Cuisine.objects.all();
    for cuisine in cuisines:
        cuisine_list.append(cuisine.cuisine_type)
    return JsonResponse({"cuisines":cuisine_list})


#function to increment the value in last index of rating_floor and retuen the real average rating for recipe for sorting purposes
#used in search method
    
def true_floor(x):
    if x["rating_floor"]!=[]:
        floor_range = x["rating_floor"]
        floor = floor_range[-1]+1
        
        return floor + 0.5
    else:
        return 0;


#view for browse and search results
def search(request,cuisine="",category="all",level=-1,userid=""):
    cuisine_list = []
    #checking if any user has logged in
    username,logged_in = check_logged_in(request)
    
    # name to be displayed  in the template in case the user has browsed any section  
    display_name = ""
    if cuisine!="":
        display_name = cuisine.title()
    if category!="all":
        display_name = category.title()
    if level!=-1:
        display_name = level.title()
    
    #retrieving all cuisine objects
    cuisines = Cuisine.objects.all();
    for c in cuisines:
        cuisine_list.append(c.cuisine_type.lower())
    
    context_dict={}
    
    #retrieving the recipes
    recipes=[]
    Recipes = Recipe.objects.all();
    for i in Recipes:
        recipes.append(i)
        
    name="All"
    
    if request.method=="POST":
        #input given in search bar
        name = request.POST.get("search")
        #cuisine selected by user
        cuisine=request.POST.get("cuisine")
        #level selected by user
        level=request.POST.get("Level")
        #category seleted by user
        category=request.POST.get("category")
    if name!="All" and name!="" and name!="" and name!=None:
        #if search bar is not empty retrieve the recipes which contains the keyword
        recipes = Recipe.objects.filter(recipe_name__icontains=name)
        
    if cuisine.lower() in cuisine_list:
        #filtering the recipe list based on cuisine
        recipe_temp = []
        for i in recipes:
            print(i.cuisine)
            c = Cuisine.objects.filter(cuisine_type__iexact=cuisine)
            if i.cuisine == c[0]:
                recipe_temp.append(i)
        recipes = recipe_temp.copy()
    
    
    categories={"vegetarian":1,"vegan":2}
    levels={"beginner":0,"intermediate":1,"expert":2}    
    if category in categories.keys():
        #filtering the recipes based on category/cooking_type
        recipe_temp = []
        for i in recipes:
            if i.cooking_type == categories[category]:
                recipe_temp.append(i)
        recipes = recipe_temp.copy()
        
    if level in levels.keys():
        #filtering the recipes based on level
        recipe_temp = []
        for i in recipes:
            if i.level == levels[level]:
                recipe_temp.append(i)
        recipes =recipe_temp.copy()
    
           
    if userid!="":
        #filtering the recipe based on userid
        recipe_temp = []
        u = User.objects.filter(username=userid)
        for j in u:
            print("j :",j)
            
            recipes=Recipe.objects.filter(username=j)
            
            
            
            
    recipes_list=[]
    for recipe in recipes:
        #checking if the rating has a decimal part
        #used for displaying rating in stars
        
        decimal = [1]
        if recipe.average_rating == math.floor(recipe.average_rating):
            
            decimal=[]
        recipe_list={"id":recipe.recipe_id,
                     "name":recipe.recipe_name,
                     "username":recipe.username,
                     "rating_ceil":list(range(5-math.ceil(recipe.average_rating))),#to get the number of coloured star in rating
                     "rating_floor":list(range(math.floor(recipe.average_rating))),#to get the number of blank stars in rating
                     "rating_decimal":decimal,
                     "path":"/breakingbread/recipe/"+str(recipe.recipe_id)}
                     
        
        #retrieving the first image of each recipe
        images = Image.objects.filter(recipe_id=recipe.recipe_id)
        for image in images:
            recipe_list["image"]=image.picture
            break
        recipes_list.append(recipe_list)

    #sort the list based on rating
    recipes_list.sort(key=lambda x:true_floor(x),reverse=True)   
    context_dict["recipes"]=recipes_list
    context_dict["cuisines"]= [i.title() for i in cuisine_list ]
    
    if name==None:
        name="All"
    context_dict["name"]=name
    context_dict["cuisine"]=cuisine
    context_dict["category"]=category
    context_dict["categories"]=["Vegetarian","Vegan","All"]
    context_dict["level"]=level
    context_dict["levels"]=["Beginner","Intermediate","Expert"]
    if userid=="":
        userid = 0
    context_dict["user"]=userid
    context_dict["nav_tab"]="search"
    context_dict["logged_in"]=logged_in
    context_dict["username"]=username
    context_dict["display_name"]=display_name
    response = render(request, 'breakingbread/search-results.html',context=context_dict)
    return response

#user details
@login_required
def user_details(request) :
    context_dict= {}
    updateSuccess = False
    current_profile = []
    # check if logged in user has an entry in UserProfile table
    # users logged in through google would have an entry only in User model and not UserProfile model
    try:
       current_profile = UserProfile.objects.get(user=request.user)
     #insert a new entry in UserProfile, in case the user does not have one
    except UserProfile.DoesNotExist:
        new_profile = { 'user': request.user,
                'usertype': 0,
                'address': '',
                'picture': ''
                }
        user = UserProfile.objects.get_or_create(user = new_profile['user'])[0]
        user.usertype = new_profile['usertype']
        user.address = new_profile['address']
        user.picture = new_profile['picture']
        user.save()
        current_profile = UserProfile.objects.get(user=request.user)

    #updating the userprofile details in the database 
    if request.method=="POST":
        request.user.first_name = request.POST.get('firstname')
        request.user.last_name  = request.POST.get('lastname')
        request.user.email  = request.POST.get('email')
        address = request.POST.get('address')
        if 'picture' in request.FILES:
            current_profile.picture = request.FILES['picture']
            

        current_profile.address = address
        request.user.save()
        current_profile.save()
        updateSuccess = True
            

    context_dict = {"profile" : current_profile, "updateSuccess" : updateSuccess}
    
    return render(request, 'breakingbread/user-details.html',context=context_dict)

#view for uploading new recipe
@login_required
def upload_recipe(request) :
    # upload images for the created recipe 
    # POST required to upload images
    if request.method == "POST":
        images = []
        recipe = Recipe.objects.get(recipe_id=request.POST.get('recipeId'))
        number = int(request.POST.get('number'))
        for i in range(number) :
            imageId = 'image' + str(i)
            if imageId in request.FILES :
                image = Image(
                    picture =  request.FILES[imageId],
                    recipe_id = recipe
                )
                image.save()
                images.append(image)

        
        data = {
            
            "success" : True,
        }
        return JsonResponse(data)
        print('request.FILES', request.FILES)

    else :
        #get the fields and create new recipe
        recipeName = request.GET.get('recipeName', None)
        cuisine = request.GET.get('cuisine', None)
        time_taken = request.GET.get('time_taken', None)
        cooking_type = request.GET.get('type', None)
        level = request.GET.get('level', None)
        ingredients = request.GET.get('ingredients', None)
        # category = request.GET.get('category', None)
        desc = request.GET.get('desc', None)
        print(cuisine)
        recipe = Recipe(
            recipe_name = recipeName,
            username =  request.user,
            time_taken = time_taken,
            level = int(level),
            ingredients = ingredients,
            cooking_type = int(cooking_type),
            
            cuisine = Cuisine.objects.filter(cuisine_type=cuisine)[0],
            description = desc,
            created = datetime.datetime.now()
        )

        recipe.save()
        data = {
        #    "recipeId" : recipe.recipe_id,
            "recipeId" : recipe.recipe_id,
        }

        return JsonResponse(data)

#about page
def about(request):
    #retrieving the different types of recipes' count
    nb_burger_recipes = Recipe.objects.filter(recipe_name__icontains="burger").count()
    nb_all_recipes = Recipe.objects.all().count()
    nb_meat_recipes = Recipe.objects.filter(cooking_type = "0").count()
    nb_vegan_recipes = Recipe.objects.filter(cooking_type = "2").count()
    context_dict = {"nb_burgers" : nb_burger_recipes, "nb_recipes" : nb_all_recipes, "nb_meats":nb_meat_recipes, "nb_vegans":nb_vegan_recipes, "nav_tab":"about"}
    return render(request, 'breakingbread/about.html', context = context_dict)

#delete recipe
def delete_recipe(request, recipe_id):
    recipe = Recipe.objects.get(recipe_id=recipe_id)  # Get your current recipe

    if request.method == 'POST':         # If method is POST,
        recipe.delete()                     # delete the recipe
        return redirect('/')             # Finally, redirect

    return render(request, '/')
    # If method is not POST, render the default template.
   