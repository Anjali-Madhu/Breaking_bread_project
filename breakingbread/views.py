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

def recipe(request,recipe_name_slug):
    return render(request, 'breakingbread/receipe-post.html')

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
def search(request,cuisine="",category="all",level=-1,userid=""):
    cuisine_list = []
    #retrieving the cuisine list
    
    
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
        for i in recipes:
            u = User.objects.filter(username=userid)
            if i.username==u:
                recipe_temp.append(i)
        recipes = recipe_temp.copy()
    recipes_list=[]
    for recipe in recipes:
        #checking if the rating has a decimal part
        #print(recipe)
        decimal = [1]
        if recipe.average_rating == math.floor(recipe.average_rating):
            #print(recipe.average_rating,math.floor(recipe.average_rating))
            decimal=[]
        recipe_list={"id":recipe.recipe_id,
                     "name":recipe.recipe_name,
                     "username":recipe.username,
                     "rating_ceil":list(range(5-math.ceil(recipe.average_rating))),#to get the number of coloured star in rating
                     "rating_floor":list(range(math.floor(recipe.average_rating))),#to get the number of blank stars in rating
                     "rating_decimal":decimal,}
                     #"slug":recipe.slug}
        #print(decimal)
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
    response = render(request, 'breakingbread/search-results.html',context=context_dict)
    return response

#user details
@login_required
def user_details(request) :
    context_dict= {}
    updateSuccess = False
    if request.method=="POST":
        request.user.first_name = request.POST.get('firstname')
        request.user.last_name  = request.POST.get('lastname')
        request.user.email  = request.POST.get('email')
        address = request.POST.get('address')
        request.user.save()
        UserProfile.objects.filter(user=request.user).update(address=address)
        updateSuccess = True
            # profile.picture = request.FILES['picture']
        # context_dict{"updateSuccess" : updateSuccess}

    current_profile = UserProfile.objects.get(user=request.user)
    context_dict = {"profile" : current_profile, "updateSuccess" : updateSuccess}
    #  context_dict={"user":current_user.username}
    return render(request, 'breakingbread/user-details.html',context=context_dict)
    


