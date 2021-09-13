from django.test import TestCase

from .models import Image, Profile, Comment
from django.contrib.auth.models import User


class TestProfile(TestCase):
    def setUp(self):
        self.user = User(username='charles')
        self.user.save()

        self.profile_test = Profile(id=1, name='image', profile_pic='avartar.jpg', bio='feeling myself',
                                    user=self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile_test, Profile))

    def test_save_profile(self):
        self.profile_test.save_profile()
        after = Profile.objects.all()
        self.assertTrue(len(after) > 0)


class TestPost(TestCase):
    def setUp(self):
        self.profile = Profile(name='Franklin Mutua', user=User(username='Frankfreek'))
        self.profile.save()

        self.image_post = Image(image='avartar.jpg', image_name='avartar', image_caption='new avartars', posted_by=self.profile)

    def test_instance(self):
        self.assertTrue(isinstance(self.image_post, Image))

    def test_save_image(self):
        self.image_post.save_image()
        images = Image.objects.all()
        self.assertTrue(len(images) > 0)

    def test_delete_image(self):
        self.image_post.delete_image()
        result = Profile.objects.all()
        self.assertTrue(len(result) < 1)