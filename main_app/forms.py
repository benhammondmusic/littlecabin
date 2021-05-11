from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


# custom form to register user with first/last names required, and username displayed as "email"
class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    # username = forms.EmailField()

    class Meta:
        model = User
        labels = {"username": "Email" } #"groups": "Owner Group"
        fields = ('username','first_name','last_name',  'password1' ,'password2' )   #'groups',


# custom login form to display username as "email"
class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )