# Generated by Django 3.2.3 on 2021-05-27 04:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0009_alter_user_pfp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1955), django.core.validators.MaxValueValidator(2021)])),
                ('make', models.CharField(max_length=20)),
                ('model', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='make',
        ),
        migrations.RemoveField(
            model_name='post',
            name='model',
        ),
        migrations.RemoveField(
            model_name='post',
            name='year',
        ),
        migrations.AlterField(
            model_name='user',
            name='pfp',
            field=models.ImageField(default='/img/pfp.png', upload_to='img/'),
        ),
        migrations.AddField(
            model_name='user',
            name='my_vehicles',
            field=models.ManyToManyField(related_name='people_who_own', to='users_app.Vehicle'),
        ),
    ]