from typing import ContextManager
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Image, Profile, User, Comment
from .forms import UserRegistrationForm, ImagePostForm, CommentForm, UpdateUserProfileForm, UpdateUserForm
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
    images = Image.objects.all().order_by('-posted_on')
    current_user = request.user

    if request.method == 'POST':
        iForm = ImagePostForm(request.POST, request.FILES)
        if iForm.is_valid():
            image_post = iForm.save(commit=False)
            image_post.posted_by = current_user
            image_post.save()
            return redirect('home')
    else:
        iForm = ImagePostForm()
    
    title ='Home'
    context ={
        "images":images,
        "title":title,
        "iForm":iForm
    }

    return render(request, 'gram/index.html', context)


class postImages(ListView):
    model=Image
    template_name='gram/index.html'

class postImageDetails(DetailView):
    model=Image
    template_name ='gram/postDetails.html'


@login_required(login_url='login')
def profile(request, username):
    # profiles = Profile.objects.get(username=username)
    profiles = get_object_or_404(User, username=username)
    users = Profile.objects.all()
    print(users)
    # userProfiles = Profile.objects.get(user=request.user.id)



    print(profiles)
    title ='Profile'
    context ={
        "title":title,
        "profiles":profiles,
        "users":users,
        # "userProfiles":userProfiles
    }

    return render(request, 'profile/myProfile.html', context)

@login_required(login_url='login')
def myProfile(request, id):
    # profiles = get_object_or_404(User, username=username)
    # users = Profile.objects.all()
    # posts = request.user.profile.posts.all()
    profile = Profile.objects.get(id =id)

    print(profile)
    

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('home')
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)


    print(profiles)
    title ='Profile'
    context ={
        "title":title,
        "profiles":profiles,
        "users":users,
        # "userProfiles":userProfiles
    }

    return render(request, 'profile/userProfile.html', context)


def single_post(request, id):

    current_user = request.user
    post = get_object_or_404(Image, id=id)
    # comments= get_object_or_404(Comment, id=id)
    print(post)
    if request.method == 'POST':
        cForm = CommentForm(request.POST)
        if cForm.is_valid():
            new_comment = cForm.save(commit=False)
            new_comment.image = post
            new_comment.posted_by = current_user
            new_comment.save()
            return redirect('home')
    else:
        cForm = CommentForm()
    context = {
        'image': post,
        'cForm': cForm,
        # 'comments':comments
        
    }

    return render(request, 'gram/singlePost.html', context )

class SinglePostView(DetailView):
    models = Image
    template_name = 'gram/singlePost.html'

    def get_queryset(self): 
        return Image.objects.all()

@login_required(login_url='login')
def add_comment(request, id):
    current_user = request.user
    image = get_object_or_404(Image, pk=id)
   
    if request.method == 'POST':
        cForm = CommentForm(request.POST)
        if cForm.is_valid():
            new_comment = cForm.save(commit=False)
            new_comment.image = image
            new_comment.user = current_user
            new_comment.save()
            return redirect('home')
    else:
        cForm = CommentForm()
    context = {
        'image': image,
        'cForm': cForm,
        
    }
    return render(request, 'gram/singlePost.html', context)

