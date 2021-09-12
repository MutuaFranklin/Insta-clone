from django.contrib import admin
from .models import Follow, Image, Profile, Comment

# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    filter_horizontal =('likes',)

class FollowAdmin(admin.ModelAdmin):
    filter_horizontal =('following','followers')


admin.site.register(Profile)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment)


