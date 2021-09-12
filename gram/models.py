from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# from cloudinary.models import CloudinaryField



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(blank=True, max_length=120)
    profile_pic = models.ImageField(upload_to = 'instaPhotos',default='avartar.jpg')
    bio = models.TextField(blank= True)
    followers = models.ManyToManyField('Follow',related_name="user_followers", blank=True)
    following = models.ManyToManyField('Follow',related_name="user_following",blank=True)

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
            self.save()

        

   
   

    @classmethod
    def search_user(cls, username):
        image= cls.objects.filter(user__username__icontains=username)
        return image


class Image(models.Model):
    # image = CloudinaryField('image')
    image= models.ImageField(upload_to ='instaPhotos', default='avartar.png')
    image_name =models.CharField(max_length=100)
    image_caption =models.TextField(blank= True)
    likes = models.ManyToManyField(Profile, related_name="like", blank= True)
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_user')
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_name

    def save_image(self):
        self.save()
    
    def delete_image(self):
        self.delete()


    def update_caption(self, updated_caption):
        self.caption = updated_caption
        self.save()

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-posted_on']



class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete= models.CASCADE, related_name='comments')
    comment = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def save_comment(self):
        self.save()

    def delete_comment(self):
            self.delete()


    class Meta:
        ordering = ['-posted_on']


    
class Follow(models.Model):
    following = models.ManyToManyField(Profile, blank= True, related_name='user_following')
    followers = models.ManyToManyField(Profile, blank= True, related_name='user_followers')

    


