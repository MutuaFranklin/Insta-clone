from django.test import TestCase
from django.contrib.auth.models import User
from .models import Image, Comment, Profile

class TestAppModelsClass(TestCase):
    def setUp(self):
        self.frank = User(id = 134, username = "frank", email = "frankngumbi@gmail.com",password = "1234567")
        self.frank.save()

        self.profile = Profile(id= 5, user= self.frank, bio='myself',  profile_pic='frank.jpg')
        self.profile.save()

      # self.profile = Profile(bio='old monk', user= self.frankfreek,followers = 'Widget', following='Widget')
        self.honda = Image(id= 3, image = 'honda.jpg', image_name ='honda', image_caption = 'Noma', posted_by = self.profile)
        self.honda.save()

        self.comment = Comment(id = 5, image=self.honda, comment= 'dopeness', posted_by = self.frank)
        self.comment.save_comment()
   
    # Teardown
    def tearDown(self):
        User.objects.all().delete()
        Image.objects.all().delete()
        Profile.objects.all().delete()
        Comment.objects.all().delete()

    # Instances

    def test_user_instance(self):
        self.assertTrue(isinstance(self.frank, User))

    def test_profile_instance(self):
         self.assertTrue(isinstance(self.profile, Profile))

    def test_image_instance(self):
        self.assertTrue(isinstance(self.honda, Image))

    def test_instance(self):
            self.assertTrue(isinstance(self.comment, Comment))

    # Save method
    def test_save_Profile(self):
        self.profile.save()
        images = Image.objects.all()
        self.assertTrue(len(images)> 0)

    def test_save_image(self):
        self.honda.save()
        images = Image.objects.all()
        self.assertTrue(len(images)> 0)

    def test_save_comment(self):
        self.comment.save_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments)> 0)


    #Update method
    def test_update_images(self):
        self.honda.save()
        image = Image.objects.last().id
        Image.update_caption(image,'I want this')
        update_image = Image.objects.get(id = image)
        self.assertEqual(update_image.image_caption,'I want this') 

    def test_update_image_caption(self):
        self.honda.save()
        self.honda.update_caption('I want this')
        self.assertEqual(self.honda.caption, 'I want this')

    def test_update_profile(self):
        self.profile.save()
        profile = Profile.objects.last().id
        Profile.update_prof_bio(profile,'The man')
        update_profile = Profile.objects.get(id = profile)
        self.assertEqual(update_profile.bio,'The man')

    

    #Delete Method
    def test_delete_image(self):
        before_del = Image.objects.all()
        self.assertEqual(len(before_del),1)
        self.honda.delete_image()
        after_del = Image.objects.all()
        self.assertEqual(len(after_del),0)

    def test_delete_comment(self):
        before_del = Comment.objects.all()
        self.assertEqual(len(before_del),1)
        self.comment.delete_comment()
        after_del  = Comment.objects.all()
        self.assertTrue(len(after_del)==0)

    #search
    def test_search_user(self):
        user = Profile.search_user(self.frank)
        self.assertEqual(len(user), 1)


   

