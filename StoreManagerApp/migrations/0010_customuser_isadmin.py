# Generated by Django 4.1.7 on 2023-05-17 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoreManagerApp', '0009_customuser_isadvertiser_customuser_issimpleuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='IsAdmin',
            field=models.BooleanField(default=False),
        ),
    ]
