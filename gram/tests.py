from django.test import TestCase
from django.contrib.auth.models import User
from .models import Image, Comment, Profile

class ImageTestClass(TestCase):
    def setUp(self):
        self.frank = User(username = "frank", email = "frankngumbi@gmail.com",password = "1234567")
        self.profile = Profile(bio='old monk', user= self.frank)
        # self.profile = Profile(bio='old monk', user= self.frankfreek,followers = 'Widget', following='Widget')
        self.honda = Image(image = 'honda.jpg', image_name ='honda', image_caption = 'Noma', posted_by = self.profile)

        self.frank.save()
        self.profile.save()
        self.honda.save()

    def tearDown(self):
        Image.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.honda, Image))

    def test_save_image(self):
        images = Image.objects.all()
        self.assertTrue(len(images)> 0)

    def test_update_image_caption(self):
        self.honda.update_caption('I want this')
        self.assertEqual(self.honda.caption, 'I want this')

    def test_delete_image(self):
        before_del = Image.objects.all()
        self.assertEqual(len(before_del),1)
        self.audi.delete_image()
        after_del = Image.objects.all()
        self.assertEqual(len(after_del),0)

    

    # def test_get_profile_images(self):
    #     self.audi.save_image()
    #     images = Image.get_profile_images(self.profile)
    #     self.assertEqual(len(images),2)

class ProfileTestClass(TestCase):
    def setUp(self):
        self.frank = User(username = "frank", email = "frankngumbi@gmail.com",password = "1234567")
        self.profile = Profile(bio='myself', user= self.frank)

        # self.profile = Profile(bio='old monk', user= self.frankfreek, followers = 'Widget', following='Widget')
        self.frank.save()

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.frank, User))
        self.assertTrue(isinstance(self.profile, Profile))

    def test_search_user(self):
        user = Profile.search_user(self.frank)
        self.assertEqual(len(user), 1)

class CommentTestClass(TestCase):
    def setUp(self):
        self.frank = User(username = "frank", email = "frankngumbi@gmail.com",password = "1234567")
        self.profile = Profile(bio='myself', user= self.frank)

        self.honda = Image(image = 'honda.jpg', image_name ='honda', image_caption = 'Noma', posted_by = self.profile)
    
        self.comment = Comment(image=self.honda, comment= 'dopeness', posted_by = self.frank)

        self.frank.save()
        self.profile.save()
        self.honda.save_image()
        self.comment.save_comment()

    def tearDown(self):
        Image.objects.all().delete()
        Profile.objects.all().delete()
        Comment.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.comment, Comment))

    def test_save_comment(self):
        self.comment.save_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments)> 0)

    def test_delete_comment(self):
       
        self.honda.save_image()
        self.comment.save_comment()
        before_del = Comment.objects.all()
        self.assertEqual(len(before_del),1)
        self.comment.delete_comment()
        after_del = Comment.objects.all()
        self.assertEqual(len(after_del),0)

    # def test_get_image_comments(self):
    #     comments = Comment.get_image_comments(self.audi)
    #     self.assertEqual(comments[0].content, 'I want this')
    #     self.assertTrue(len(comments) > 0)

