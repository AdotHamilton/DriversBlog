# Generated by Django 3.2.3 on 2021-05-22 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0004_auto_20210510_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pfp',
            field=models.ImageField(default='./static/img/pfp.jpg', height_field=170, upload_to='pfps', width_field=170),
        ),
    ]
