from django import forms
from breakingbread.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#different types of users
user_types=[(0,'Regular'),(1,'Chef'),(2,'Restaurant')]

#form for registeration
class SignUpForm(UserCreationForm):
    username=forms.CharField(max_length=128,required=True, widget=forms.TextInput())
    first_name=forms.CharField(max_length=30,required=True,widget=forms.TextInput())
    last_name=forms.CharField(max_length=30,required=True,widget=forms.TextInput())
    email = forms.EmailField(max_length=40,required=True,widget=forms.TextInput())
    password1=forms.CharField(label = "Password",widget=forms.PasswordInput(),required=True)
    password2=forms.CharField(label = "Confirm Password",widget=forms.PasswordInput(),required=True)
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1','password2')
 
#form for registeration("usertype, address, profile picture fields)       
class UserProfileForm(forms.ModelForm):
    
    usertype=forms.CharField(label="User Type  ",widget=forms.Select(choices=user_types),)
    usertype.widget.attrs.update({'class':'form-control'})
    address = forms.CharField(max_length=100,widget=forms.TextInput())
    
    class Meta:
        model=UserProfile
        fields=('usertype','address','picture',)







