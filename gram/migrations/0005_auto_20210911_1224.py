# Generated by Django 3.2.7 on 2021-09-11 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gram', '0004_alter_image_posted_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-posted_on']},
        ),
        migrations.AlterField(
            model_name='image',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gram.profile'),
        ),
    ]
