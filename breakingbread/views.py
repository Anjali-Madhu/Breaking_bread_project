from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,JsonResponse
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
    
    context_dict={"logged_in":logged_in, "username":username, "best_recipes": best_recipes_images,
                 "best_vegan": best_vegan, "best_vegetarian":best_vegetarian, "nav_tab":"home"}
    response = render(request, 'breakingbread/index.html', context=context_dict)
    return response

def register(request):
    registered=False
    if request.method=="POST":
        user_form=SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # print('userform ', user_form)
            # user = user_form.save()
            # print('passs', user.password)
            # user.set_password(user.password)
            user = user_form.save()
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
    context_dict = {'user_form':user_form,'profile_form':profile_form,'registered':registered, "nav_tab":"register"}
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
                print('error')
                return render(request, 'breakingbread/login.html',context={"error":"Your account has been disabled"})
                #return HttpResponse("Your account is disabled.")
        else:
            print('invalid')
            #print(f"Invalid login details: {username}, {password}")
            #return HttpResponse("Incorrect username or password")
            return render(request, 'breakingbread/login.html',context={"error":"Incorrect username or password!"})
    else:
        return render(request, 'breakingbread/login.html', context ={"nav_tab":"log_in"})
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('breakingbread:index'))

#function to increment the value in last index of rating_floor for sorting
def true_floor(x):
    if x["rating_floor"]!=[]:
        floor_range = x["rating_floor"]
        floor = floor_range[-1]+1
        
        return floor + 0.5
    else:
        return 0;

def recipe(request,recipe_id):
    logged_in=False
    username=""
  
    if request.user.is_authenticated:
        logged_in=True
        username=request.user.username
    else:
        logged_in=False
        
    
    recipe_to_display = Recipe.objects.filter(recipe_id= recipe_id)
    
    #rating     
    decimal = [1]
    if recipe_to_display[0].average_rating == math.floor(recipe_to_display[0].average_rating):
        #print(recipe.average_rating,math.floor(recipe.average_rating))
        decimal=[]
    recipe_ = {"id": recipe_to_display[0].recipe_id,
                        "name": recipe_to_display[0].recipe_name,
                        "user": recipe_to_display[0].username,
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
    images = Image.objects.filter(recipe_id=recipe_id)
    for image in images:
        recipe_["images"].append(image.picture)

    for i in recipe_to_display[0].description.split("?"):
        recipe_["description"].append(i)

    for i in recipe_to_display[0].ingredients.split("?"):
        recipe_["ingredients"].append(i)
        
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
    recipe_["reviews"] = review_list

    return render(request, 'breakingbread/receipe-post.html', context = recipe_)

@login_required
def review(request,recipe_id):
    form = ReviewForm()
    recipe_page = Recipe.objects.filter(recipe_id= recipe_id)
    #reviews =
    if request.method == 'POST':
               
        description = request.POST.get("message")
        rating = request.POST.get("stars")
        review = Review(recipe_id=recipe_page[0],username=request.user,description=description)
        review.save()
        print(description,rating,request.user,recipe_id)
    #return render(request, 'breakingbread/recipe/'+str(recipe_id), {'form': form})
    response = recipe(request,recipe_id)
    return response
    
def cuisine_list(request):
    #checking if any user has logged in 
    
    cuisine_list=[];
    #retrieving the cuisine list
    cuisines = Cuisine.objects.all();
    for cuisine in cuisines:
        cuisine_list.append(cuisine.cuisine_type)
    return JsonResponse({"cuisines":cuisine_list})


#retrieving search results
def search(request,cuisine="",category="all",level=-1,userid=""):
    cuisine_list = []
    #retrieving the cuisine list
    logged_in=False
    username=""
  
    if request.user.is_authenticated:
        logged_in=True
        username=request.user.username
    else:
        logged_in=False
        
    display_name = ""
    if cuisine!="":
        display_name = cuisine
    if category!="all":
        display_name = category
    if level!=-1:
        display_name = level
    
    
    cuisines = Cuisine.objects.all();
    for c in cuisines:
        cuisine_list.append(c.cuisine_type)
    context_dict={}
       #retrieving the recipes
    recipes=[]
    Recipes = Recipe.objects.all();
    for i in Recipes:
        recipes.append(i)
        
    name="All"
    
    if request.method=="POST":
        
        name = request.POST.get("search")
        
        cuisine=request.POST.get("cuisine")
        level=request.POST.get("Level")
        category=request.POST.get("category")
    if name!="All" and name!="" and name!="" and name!=None:
        recipes = Recipe.objects.filter(recipe_name__icontains=name)
        
    if cuisine in cuisine_list:
        print("Cuisine : ",cuisine)
        recipe_temp = []
        for i in recipes:
            print(i.cuisine)
            c = Cuisine.objects.filter(cuisine_type=cuisine)
            if i.cuisine == c[0]:
                recipe_temp.append(i)
        recipes = recipe_temp.copy()
    
    
    categories={"Vegetarian":1,"Vegan":2}
    levels={"Beginner":0,"Intermediate":1,"Expert":2}    
    if category in categories.keys():
        recipe_temp = []
        for i in recipes:
            if i.cooking_type == categories[category]:
                recipe_temp.append(i)
        recipes = recipe_temp.copy()
        
    if level in levels.keys():
        recipe_temp = []
        for i in recipes:
            if i.level == levels[level]:
                recipe_temp.append(i)
        recipes =recipe_temp.copy()
    
           
    if userid!="":
        recipe_temp = []
        u = User.objects.filter(username=userid)
        for j in u:
            print("j :",j)
            
            recipes=Recipe.objects.filter(username=j)
            
            
            
            
    recipes_list=[]
    for recipe in recipes:
        #checking if the rating has a decimal part
        print(recipe)
        
        decimal = [1]
        if recipe.average_rating == math.floor(recipe.average_rating):
            #print(recipe.average_rating,math.floor(recipe.average_rating))
            decimal=[]
        recipe_list={"id":recipe.recipe_id,
                     "name":recipe.recipe_name,
                     "username":recipe.username,
                     "rating_ceil":list(range(5-math.ceil(recipe.average_rating))),#to get the number of coloured star in rating
                     "rating_floor":list(range(math.floor(recipe.average_rating))),#to get the number of blank stars in rating
                     "rating_decimal":decimal,
                     "path":"/breakingbread/recipe/"+str(recipe.recipe_id)}
                     #"slug":recipe.slug}
        #print(decimal)
        #retrieving the first image of each recipe
        images = Image.objects.filter(recipe_id=recipe.recipe_id)
        for image in images:
            recipe_list["image"]=image.picture
            break
        recipes_list.append(recipe_list)

    #sort the list based on rating
    recipes_list.sort(key=lambda x:true_floor(x),reverse=True)   
    context_dict["recipes"]=recipes_list
    context_dict["cuisines"]= cuisine_list
    
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
    
    try:
       current_profile = UserProfile.objects.get(user=request.user)
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


    if request.method=="POST":
        request.user.first_name = request.POST.get('firstname')
        request.user.last_name  = request.POST.get('lastname')
        request.user.email  = request.POST.get('email')
        address = request.POST.get('address')
        if 'picture' in request.FILES:
            current_profile.picture = request.FILES['picture']
            # UserProfile.objects.filter(user=request.user).update(picture=request.FILES['picture'])

        current_profile.address = address
        request.user.save()
        current_profile.save()
        updateSuccess = True
            # profile.picture = request.FILES['picture']
        # context_dict{"updateSuccess" : updateSuccess}

    context_dict = {"profile" : current_profile, "updateSuccess" : updateSuccess}
    #  context_dict={"user":current_user.username}
    return render(request, 'breakingbread/user-details.html',context=context_dict)

@login_required
def upload_recipe(request) :
    # for images
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

        # print('num', request.POST.get('number'))
        data = {
            # "images": images,
            "success" : True,
        }
        return JsonResponse(data)
        print('request.FILES', request.FILES)

    else :
        #get the fields
        recipeName = request.GET.get('recipeName', None)
        cuisine = request.GET.get('cuisine', None)
        time_taken = request.GET.get('time_taken', None)
        cooking_type = request.GET.get('type', None)
        level = request.GET.get('level', None)
        ingredients = request.GET.get('ingredients', None)
        # category = request.GET.get('category', None)
        desc = request.GET.get('desc', None)
        recipe = Recipe(
            recipe_name = recipeName,
            username =  request.user,
            time_taken = time_taken,
            level = level,
            ingredients = ingredients,
            cooking_type = cooking_type,
            cuisine = Cuisine.objects.get(cuisine_type=cuisine),
            description = desc,
            created = datetime.datetime.now()
        )

        recipe.save()
        data = {
        #    "recipeId" : recipe.recipe_id,
            "recipeId" : recipe.recipe_id,
        }

        return JsonResponse(data)


def about(request):
    
    nb_burger_recipes = Recipe.objects.filter(recipe_name__icontains="burger").count()
    nb_all_recipes = Recipe.objects.all().count()
    nb_meat_recipes = Recipe.objects.filter(cooking_type = "0").count()
    nb_vegan_recipes = Recipe.objects.filter(cooking_type = "2").count()
    context_dict = {"nb_burgers" : nb_burger_recipes, "nb_recipes" : nb_all_recipes, "nb_meats":nb_meat_recipes, "nb_vegans":nb_vegan_recipes, "nav_tab":"about"}
    return render(request, 'breakingbread/about.html', context = context_dict)