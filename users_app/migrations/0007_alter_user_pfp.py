# Generated by Django 3.2.3 on 2021-05-25 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0006_auto_20210525_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pfp',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
