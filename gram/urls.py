from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path, include
from .views import follow_actions, logout, postImageDetails, postImages, postLike, signIn, SinglePostView, single_post


urlpatterns=[
    path('', views.signIn, name='login'),
    path('register/', views.register, name='register'),
    path('account/', include('django.contrib.auth.urls')),
    re_path(r'home/', views.home, name='home'),
    path('image-details/<int:pk>',SinglePostView.as_view(), name='image-details'),
    path('comment/<int:id>',single_post, name='comment'),
    path('logout/',views.logout, name='logout'),
    path('profile/<username>/', views.profile, name='profile'),
    path('', views.editProfile, name='edit-profile'),
    path('userprofile/<username>/', views.userProfile, name='userProfile'),
    path('search/', views.search_user, name='search_user'),
    path('like/<int:pk>', postLike, name = 'post_like'),
    path('follow', follow_actions, name = 'follow_actions'),





    # path('follow/<follow_action>', views.follow, name='follow'),
    # path('unFollow/<unFollow_action>', views.unFollow, name='unFollow'),
    # path('home/', postImages.as_view(), name = 'home'),
    # re_path(r'profile', views.userProfile, name='profile'),
    # re_path(r'profile/(?P<user_id>\d+)',views.userProfile,name = 'profile'),
    # re_path('profile/<username>/', views.userProfile, name='profile'),



   


]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


