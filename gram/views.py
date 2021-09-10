from typing import ContextManager
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Image, Profile, User
from .forms import UserRegistrationForm, UpdateUserProfileForm, UpdateUserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.
def register(request):
    reg_form = UserRegistrationForm()
    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            user = reg_form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    title = 'Registration'
    # context ={
    #     "title":title,
    #     'reg_form,': reg_form
    # }

    
    return render(request, 'registration/registration.html', {'reg_form': reg_form})

def signIn(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')

    title = 'Login'
    context ={
        "title":title,
    }

   
    return render(request, 'registration/login.html', context)

def logout(request):
    return redirect('login')


def home(request):
    images = Image.objects.all()
    # users = Profile.objects.exclude(id=request.user.id)
    title ='Home'
    context ={
        "images":images,
        "title":title,
        # "users":users
    }

    return render(request, 'gram/index.html', context)


class postImages(ListView):
    model=Image
    template_name='gram/index.html'

class postImageDetails(DetailView):
    model=Image
    template_name ='gram/postDetails.html'


@login_required(login_url='/accounts/login/')
def userProfile(request, username):
    # pitches = Pitch.query.filter_by(user=current_user)
    # imagePosts = 
    # profiles = Profile.objects.get(username=username)
    profiles = get_object_or_404(User, username=username)
    print(profiles)
    title ='Profile'
    context ={
        "title":title,
        "profiles":profiles
    }

    return render(request, 'profile/userProfile.html', context)

