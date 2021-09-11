from django.db import models
from django.contrib.auth.models import User
# from cloudinary.models import CloudinaryField



# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=120)
    profile_pic = models.ImageField(upload_to = 'instaPhotos', blank= True)
    bio = models.TextField(blank= True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def save_profile(self):
            self.save()

    @classmethod
    def search_user(cls,user): 
        return User.objects.filter(user = user)


class Image(models.Model):
    # image = CloudinaryField('image')
    image= models.ImageField(upload_to ='instaPhotos', default='avartar.png')
    image_name =models.CharField(max_length=100)
    image_caption =models.TextField(blank= True)
    likes = models.ManyToManyField(Profile, related_name="image_posts", blank= True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
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
    image = models.ForeignKey(Image, on_delete= models.CASCADE)
    comment = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def save_comment(self):
        self.save()

    def delete_comment(self):
            self.delete()


    class Meta:
        ordering = ['posted_on']


