# Generated by Django 3.2.3 on 2021-05-29 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0015_auto_20210528_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='header',
            field=models.CharField(default='Header', max_length=40),
            preserve_default=False,
        ),
    ]