# Generated by Django 4.2.6 on 2023-12-20 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_customuser_gender_customuser_interested_in_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default='no_image.jpg', null=True, upload_to='profile_pictures/'),
        ),
    ]
