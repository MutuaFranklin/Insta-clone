from typing import ContextManager
from django import contrib
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Follow, Image, Profile, User, Comment
from .forms import AddUserProfileForm, UserRegistrationForm, ImagePostForm, CommentForm, UpdateUserProfileForm, UpdateUserForm
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
        else:
            reg_form = UserRegistrationForm()
            pForm = AddUserProfileForm()

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
    current_user = request.user
    images = Image.objects.all().order_by('-posted_on')
    user = User.objects.get(username=current_user)
    profUser = Profile.objects.get(user=current_user)


    # userFollow = Follow.objects.get(user=user)
    # images = Image.objects.get(posted_by=userFollow.username).order_by('-posted_on')

   

    if request.method == 'POST':
        iForm = ImagePostForm(request.POST, request.FILES)
        if iForm.is_valid():
            image_post = iForm.save(commit=False)
            image_post.posted_by = current_user.profile
            image_post.save()
            return redirect('home')
    else:
        iForm = ImagePostForm()

   
    
    title ='Home'
    context ={
        "images":images,
        "title":title,
        "iForm":iForm,
        "user":user,
    
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
    current_user = request.user
    profiles = get_object_or_404(User, username=username)
    myProfile = Profile.objects.get(user=current_user)
    images = Image.objects.filter(posted_by = myProfile).order_by('-posted_on')


    if request.method == 'POST':
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect('profile')
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)

    # print(images)



    title ='Profile'
    context ={
        "title":title,
        "profiles":profiles,
        "myProfile":myProfile,
        "images":images,
       
    }

    return render(request, 'profile/myProfile.html', context)

@login_required(login_url='login')
def userProfile(request, username):
    otherUser = get_object_or_404(User, username=username)
    userProfile = Profile.objects.get(user=otherUser)
    images = Image.objects.filter(posted_by = userProfile).order_by('-posted_on')

    followers = Follow.objects.filter(following=otherUser.profile)
    is_followed = None
    for follower in followers:
        if request.user.profile == follower.follower:
            is_followed = True
        else:
            is_followed = False
    if request.method == 'POST':
        if 'userProf_id' in request.POST:
            userProf_id = request.POST.get('userProf_id')
            userProf = User.objects.get(id=userProf_id) 

            myProf = Profile.objects.get(user=request.user)
            myProf.following.add(userProf) 
            myProf.save()

            oProf = Profile.objects.get(user=userProf)
            oProf.followers.add(request.user)
            oProf.save()
    
    title ='User Profile'
    # context ={
    #     "title":title,
    #     "otherUser":otherUser,
    #     "userProfile":userProfile,
    #     "images": images,
    #     "is_followed":is_followed,
    #     "followers": followers
    # }

    return render(request, 'profile/userProfile.html', locals())


def single_post(request, id):

    current_user = request.user
    post = get_object_or_404(Image, id=id)
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
    all_comments = Comment.objects.all()
    comments_count= all_comments.count()
    context = {
        'image': post,
        'cForm': cForm,
        'comments_count':comments_count
        
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


def editProfile(request, username):
    current_user = request.user
    profiles = get_object_or_404(User, username=username)
    myProfile = Profile.objects.get(user=current_user)




    title="Edit profile"
    context={
        "title":title,
        "profiles":profiles,
        "myProfile":myProfile,
    }
    return render(request, 'profile/editProfile.html', context)


def search_user(request):
    if 'username' in request.GET and request.GET["username"]:
        search_username = request.GET.get("username")
        print(search_username)
        searched_users = Profile.search_user(search_username)
        print(searched_users)
        message = f"{search_username}"

        context = {
            "message":message,
            "searched_users": searched_users
        }




        return render(request, 'gram/search.html', context)

    else:
        message = "You haven't searched for any term"
        return render(request, 'gram/search.html',{"message":message})



