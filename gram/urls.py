from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path, include
from .views import logout, postImageDetails, postImages, signIn, SinglePostView, single_post


urlpatterns=[
    path('', views.signIn, name='login'),
    path('register/', views.register, name='register'),
    path('account/', include('django.contrib.auth.urls')),
    re_path(r'home/', views.home, name='home'),
    path('image-details/<int:pk>',SinglePostView.as_view(), name='image-details'),
    path('comment/<int:id>',single_post, name='comment'),
    path('logout/',views.logout, name='logout'),
    path('profile/<username>/', views.profile, name='profile'),

    # path('home/', postImages.as_view(), name = 'home'),
    # re_path(r'profile', views.userProfile, name='profile'),
    # re_path(r'profile/(?P<user_id>\d+)',views.userProfile,name = 'profile'),
    # re_path('profile/<username>/', views.userProfile, name='profile'),



   


]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


