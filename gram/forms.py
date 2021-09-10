from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from .models import Profile, Image, Comment


class UserRegistrationForm(UserCreationForm):
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        # fields="__all__"
        fields = ('first_name', 'last_name', 'email','username',  'password1', 'password2')
        widgets = {
            'first_name':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"First Name", 'label': 'First Name'}),
            'last_name':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Second Name", 'label': 'Second Name'}),
            'email':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Email Address", 'label': 'Email Address'}),
            'username':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Username", 'label': 'Username'}),
            'password1':forms.PasswordInput(attrs = {'class':'form-control ','type':'password', 'placeholder':"Password", 'label': 'Password'}),
            'password2':forms.PasswordInput(attrs = {'class':'form-control', 'placeholder':"Confirm Password", 'label': 'Confirm Password'}),
        }

# class LoginForm(forms.Mod):


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'profile_pic', 'bio']


class ImagePostForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'image_caption')


