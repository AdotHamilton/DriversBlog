# Generated by Django 3.2.3 on 2021-06-10 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0027_meet'),
    ]

    operations = [
        migrations.AddField(
            model_name='meet',
            name='state',
            field=models.CharField(max_length=2, null=True),
        ),
    ]