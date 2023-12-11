# Generated by Django 4.2.7 on 2023-12-09 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customuser_current_place_customuser_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='current_place',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='working_as',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
