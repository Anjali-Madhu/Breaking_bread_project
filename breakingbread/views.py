from django.shortcuts import render
from django.http import HttpResponse
from breakingbread.forms import *

# Create your views here.
def index(request):
    response = render(request, 'breakingbread/index.html')
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
            print(user_form.errors,profile_form.errors)
    else:
        user_form=SignUpForm()
        profile_form=UserProfileForm()
    context_dict = {'user_form':user_form,'profile_form':profile_form,'registered':registered}
    return render(request,'breakingbread/register.html',context=context_dict)