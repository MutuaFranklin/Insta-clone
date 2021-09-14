from typing import ContextManager
from django import contrib
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Follow, Image, Profile, User, Comment
from .forms import AddUserProfileForm, UserRegistrationForm, ImagePostForm, CommentForm, UpdateUserProfileForm, UpdateUserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from .email import send_welcome_email




# Create your views here.
def register(request):
    reg_form = UserRegistrationForm()



    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            user = reg_form.cleaned_data.get('username')
            email = reg_form.cleaned_data['email']
            messages.success(request, 'Account was created for ' + user)
            send_welcome_email(user,email)
            return redirect('login')
        else:
            reg_form = UserRegistrationForm()

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
    user = User.objects.get(username=current_user)
    myProfile = Profile.objects.get(user=current_user)
    images = Image.objects.all().order_by('-posted_on')
    my_posts=Image.objects.filter(posted_by = myProfile)

    # following_ids = request.user.following.values_list('id',flat=True) 


    # followed_posts=Image.objects.filter(posted_by__in = request.user.followers.all())
    followed_posts=Image.objects.filter(posted_by__in = current_user.followers.all()).all() 
    all_images = my_posts|followed_posts
    print(followed_posts)

  
   
    
   

    if request.method == 'POST':
        iForm = ImagePostForm(request.POST, request.FILES)
        if iForm.is_valid():
            image_post = iForm.save(commit=False)
            image_post.posted_by = current_user.profile
            image_post.save()
            return redirect('home')
    else:
        iForm = ImagePostForm()

   
    cForm = CommentForm(request.POST)

    title ='Home'
    context ={
        "images":all_images,
        # "images":images,
        "title":title,
        "iForm":iForm,
        "user":user,
        'cForm': cForm,
        "profile":myProfile,
      
    }


    return render(request, 'gram/index.html', context)


def suggestedProfile(request):
    profiles=Profile.objects.all()

    context={

        "profiles":profiles,
        
    }

    print(profiles)


    return render(request, 'profile/suggestedProfiles.html', context)



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
    myProfile = Profile.objects.get(user=request.user)
    images = Image.objects.filter(posted_by = userProfile).order_by('-posted_on')
    
    
    title ='User Profile'
    
    if userProfile.user in myProfile.following.all():
        follow = True
    else:
        follow = False

    if myProfile.user in userProfile.followers.all():
        follower = True
    else:
        follower = False
     

    if_following = Profile.objects.filter(following = request.user).exists()
    if_followed = Profile.objects.filter(followers =userProfile.user).exists()

    if (if_following):
        is_followed = True
    else:
        is_followed = False
    print(is_followed)

    if (if_followed):
        is_follower = True
    else:
        is_follower = False
    print(is_follower)

    context ={
        "title":title,
        "otherUser":otherUser,
        "userProfile":userProfile,
        "images": images,
        "is_followed":if_followed,
        "is_follower": is_follower,
        "follow":follow,
        "follower": follower,        
        # "is_following":if_following,
        
    }



    return render(request, 'profile/userProfile.html',  context)


def single_post(request, id):

    current_user = request.user
    post = get_object_or_404(Image, id=id)

    currentProf = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        cForm = CommentForm(request.POST)
        if cForm.is_valid():
            new_comment = cForm.save(commit=False)
            new_comment.image = post
            new_comment.posted_by = current_user
            new_comment.save()
            return HttpResponseRedirect(reverse('comment', args=[int(id)]))
            # return redirect('home')
    else:
        cForm = CommentForm()
    all_comments = Comment.objects.all()
    comments_count= all_comments.count()
    context = {
        'image': post,
        'cForm': cForm,
        'comments_count':comments_count,
        'user':current_user,
        'profile':currentProf
        
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
            new_comment.posted_by = current_user
            new_comment.save()
            return redirect('home')
    else:
        cForm = CommentForm()
    context = {
        'image': image,
        'cForm': cForm,
        
    }


    return redirect(request.META.get('HTTP_REFERER'))

def editProfile(request,id):
    updateProfile = Profile.objects.get(id=id)
    eForm = UpdateUserForm
    if request.method == 'POST':
        form = eForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = updateProfile.user.id
            post.save()
            return redirect(request.META.get('HTTP_REFERER'))

    return render(request,'profile/editProfile.html',{"form":form})

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


def postLike(request, pk):
    profile = Profile.objects.get(user=request.user)
    image_post = get_object_or_404(Image, id = request.POST.get('image_post_id'))
    image_post.likes.add(profile.user.id)

    return redirect(request.META.get('HTTP_REFERER'))

def follow_actions(request):
    if request.method == 'POST':
            if 'userProf_id' in request.POST:
                userProf_id = request.POST.get('userProf_id')
                userProf = User.objects.get(id=userProf_id) 

                myProf = Profile.objects.get(user=request.user)
                oProf = Profile.objects.get(user=userProf)


                if  oProf.user in myProf.following.all():
                    myProf.following.remove(oProf.user)
                    myProf.save()
                else:
                    myProf.following.add(userProf) 
                    myProf.save()

                if  myProf.user in oProf.followers.all():
                    oProf.followers.remove(myProf.user)
                    oProf.save()
                else:
                    oProf.followers.add(myProf.user)
                    oProf.save()

                return redirect(request.META.get('HTTP_REFERER'))