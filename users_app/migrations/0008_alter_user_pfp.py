# Generated by Django 3.2.3 on 2021-05-25 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0007_alter_user_pfp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pfp',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
    ]
