# Generated by Django 3.2.7 on 2021-09-12 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='avartar.jpg', upload_to='instaPhotos'),
        ),
    ]