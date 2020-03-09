from django import forms
from breakingbread.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

user_types=[(0,'Regular'),(1,'Chef'),(2,'Restaurant')]

class SignUpForm(UserCreationForm):
    username=forms.CharField(max_length=128,required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name=forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'FirstName'}))
    last_name=forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'LastName'}))
    email = forms.EmailField(max_length=20,required=True,widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1=forms.CharField(label = "Password",widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),required=True)
    password2=forms.CharField(label = "Confirm Password",widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),required=True)
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1','password2')
        
class UserProfileForm(forms.ModelForm):
    
    usertype=forms.CharField(label="User Type  ",widget=forms.Select(choices=user_types),)
    usertype.widget.attrs.update({'class':'form-control'})

    address = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    
    class Meta:
        model=UserProfile
        fields=('usertype','address','picture',)



