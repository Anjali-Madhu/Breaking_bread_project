from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from breakingbread.forms import *
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from breakingbread.models import *;
import json;

# Create your views here.
def index(request):
    logged_in=False
    username=""
    if request.user.is_authenticated:
        logged_in=True
        username=request.user.username
    else:
        logged_in=False
    context_dict={"logged_in":logged_in,"username":username, "c":c}
    response = render(request, 'breakingbread/index.html',context=context_dict)
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
    
    


